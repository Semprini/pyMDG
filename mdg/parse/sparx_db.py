# import enum
from typing import List, Tuple, Optional, Union
import logging
import re
from decimal import Decimal

import sqlalchemy
from sqlalchemy.orm import Session

from mdg.parse.sparx_db_models import (
    TObject,
    TPackage,
    TXref,
    TAttribute,
    TAttributeconstraint,
    TConnector,
    TAttributetag,
)

from mdg.config import settings
from mdg.uml import (
    UMLAssociation,
    UMLAttribute,
    UMLClass,
    UMLEnumeration,
    UMLInstance,
    UMLPackage,
    UMLAssociationType,
    SearchTypes,
)


logger = logging.getLogger(__name__)


def parse_uml() -> Tuple[UMLPackage, List[UMLInstance]]:
    """ Root package parser entry point.
    """
    test_cases: List[UMLInstance] = []

    engine = sqlalchemy.create_engine(f"{settings['source']}", echo=False, future=True)
    with Session(engine) as session:

        # Find the root package. Can specify either EA GUID or name
        # If guid make sure value in recipie is quoted - model_package: "{D6D3BF36-E897-4a8b-8CA9-62ADAAD696ED}"
        if settings['root_package'][0] == "{":
            stmt = sqlalchemy.select(TPackage).where(TPackage.ea_guid == settings['root_package'])
        else:
            stmt = sqlalchemy.select(TPackage).where(TPackage.name == settings['root_package'])
        root_tpackage: TPackage = session.execute(stmt).scalars().first()
        if root_tpackage is None:
            raise ValueError("Root package element not found. Settings has:{}".format(settings['root_package']))
        logger.debug(f"Root Object: {root_tpackage.package_id}: {root_tpackage.name}")

        # Find the package with the model nodes. Can specify either EA GUID or name
        # If guid make sure value in recipie is quoted - model_package: "{D6D3BF36-E897-4a8b-8CA9-62ADAAD696ED}"
        if settings['model_package'][0] == "{":
            stmt = sqlalchemy.select(TPackage).where(TPackage.ea_guid == settings['model_package'])
        else:
            stmt = sqlalchemy.select(TPackage).where(TPackage.name == settings['model_package'])
        model_tpackage: TPackage = session.execute(stmt).scalars().first()
        if model_tpackage is None:
            raise ValueError("Model package element not found. Settings has:{}".format(settings['model_package']))
        logger.debug(f"Model Object: {model_tpackage.package_id}: {model_tpackage.name}")

        root_package = package_parse(session, root_tpackage, None, False)

        # Create our model UMLPackage and parse in 3 passes
        model_package = package_parse(session, model_tpackage, root_package)
        root_package.children.append(model_package)
        logger.debug("Parsing associations and inheritance")
        package_parse_associations(session, root_package)
        logger.debug("Sorting objects")
        package_sort_classes(root_package)

    if 'test_package' in settings.keys():
        logger.info("Parsing test cases")
        if settings['test_package'][0] == "{":
            stmt = sqlalchemy.select(TPackage).where(TPackage.ea_guid == settings['test_package'])
        else:
            stmt = sqlalchemy.select(TPackage).where(TPackage.name == settings['test_package'])
        test_tpackage: TPackage = session.execute(stmt).scalars().first()
        if test_tpackage is None:
            raise ValueError("Test package element not found. Settings has:{}".format(settings['test_package']))
        test_package = package_parse(session, test_tpackage, None)
        package_parse_associations(session, test_package)
        test_package_parse_inheritance(test_package, model_package)
        test_cases = parse_test_cases(test_package)

    return root_package, test_cases


def parse_test_cases(package: UMLPackage) -> List[UMLInstance]:
    """ Looks through package hierarchy for instances with request or response stereotype
    and returns list of instances.
    """
    test_cases = []

    for instance in package.instances:
        if instance.stereotype in ['request', 'response']:
            test_cases.append(instance)

    for child in package.children:
        res = parse_test_cases(child)
        if res:
            test_cases += res

    return test_cases


def package_parse(session, tpackage: TPackage, parent_package: Optional[UMLPackage], parse_children=True):
    """ Extract package details, call class parser for classes and self parser for sub-packages.
    Associations are not done here, but in a 2nd pass using the parse_associations function.
    :param element:
    :param root_element:
    :return:
    :rtype: UMLPackage
    """

    package = UMLPackage(tpackage.package_id, tpackage.name, parent_package)

    stmt = sqlalchemy.select(TObject).where(TObject.ea_guid == tpackage.ea_guid)
    tobject = session.execute(stmt).scalars().first()

    package.stereotype = f"{tobject.stereotype}"
    if package.stereotype is not None:
        package.inherited_stereotypes.append((package.stereotype, package))

    package.documentation = tobject.note
    if package.documentation is None:
        package.documentation = ""

    package.status = tobject.status
    package.version = f"{tpackage.version}"

    logger.debug("Added UMLPackage {}".format(package.path))

    if parse_children:
        package_parse_children(session, package)
    return package


def package_parse_children(session, package: UMLPackage):
    stmt = sqlalchemy.select(TObject).where(TObject.package_id == package.id)

    # Loop through all child elements and create nodes for classes and sub packages
    for child_tobject in session.execute(stmt).scalars().all():
        if child_tobject.object_type == 'Package':
            stmt = sqlalchemy.select(TPackage).where(TPackage.ea_guid == child_tobject.ea_guid)
            tpackage = session.execute(stmt).scalars().first()
            pkg = package_parse(session, tpackage, package)
            package.children.append(pkg)

        elif child_tobject.object_type == 'Class':
            cls = class_parse(session, package, child_tobject)
            if cls.name is not None:
                package.classes.append(cls)

        elif child_tobject.object_type == 'Object':
            ins = instance_parse(session, package, child_tobject)
            if ins.name is not None:
                package.instances.append(ins)

        elif child_tobject.object_type == 'Enumeration':
            enumeration = enumeration_parse(session, package, child_tobject)
            package.enumerations.append(enumeration)


def package_parse_associations(session, package: UMLPackage):
    """ Packages and classes should already have been parsed so now we link classes for each association.
    """
    for cls in package.classes:
        stmt = sqlalchemy.select(TConnector).where(TConnector.start_object_id == cls.id)

        for connector in session.execute(stmt).scalars().all():
            dest = package.root_package.find_by_id(connector.end_object_id, SearchTypes.CLASS)
            if dest is None:
                logger.warn(f"Cannot find associated class from {cls}. Association Id:{connector.id}, Destination Id: {connector.end_object_id}")

            elif connector.connector_type in ["Association", "Aggregation"]:
                association = association_parse(session, connector, package, cls, dest)
                if association is not None:
                    package.associations.append(association)

            elif connector.connector_type == "Generalization":
                cls.generalization = dest
                dest.specialized_by.append(cls)
                if cls.id_attribute is None:
                    cls.id_attribute = dest.id_attribute

        # Find enumeration attributes of class and link to attribute
        for attr in cls.attributes:
            if attr.classification_id is not None:
                attr.classification = package.root_package.find_by_id(attr.classification_id, SearchTypes.ENUM)
                if attr.classification is None:
                    logger.warn("Cannot find expected classification for {} of attribute {}. Id={}".format(attr.dest_type, attr.name, attr.classification_id))

    for ins in package.instances:
        stmt = sqlalchemy.select(TConnector).where(TConnector.start_object_id == ins.id)

        for connector in session.execute(stmt).scalars().all():
            dest = package.root_package.find_by_id(connector.end_object_id, SearchTypes.INSTANCE)

            association = association_parse(session, connector, package, ins, dest)
            if association is not None:
                package.associations.append(association)

    for package_child in package.children:
        package_parse_associations(session, package_child)


def test_package_parse_inheritance(test_package, model_package):
    """ Links instances with the class they are instances of
        and sets the attribute types which wern't in the run_state where instance attrs are created from
    """

    for ins in test_package.instances:
        if ins.classification_id is not None:
            ins.classification = model_package.find_by_id(ins.classification_id)
            if ins.classification is None:
                ins.classification = test_package.find_by_id(ins.classification_id)
                if ins.classification is None:
                    logger.warn(f"Cannot find class which instance named {ins.name} is from id={ins.classification_id}")

            if ins.classification is not None:
                for attr in ins.attributes:
                    for cls_attr in ins.classification.attributes:
                        if attr.name == cls_attr.name:
                            attr.type = cls_attr.type
                            if attr.type.lower() in ['int', 'integer']:
                                attr.value = int(attr.value)
                            elif attr.type.lower() == ['float']:
                                attr.value = float(attr.value)
                            elif attr.type.lower() == ['decimal']:
                                attr.value = Decimal(attr.value)
                            break
        else:
            logger.warn("Instance object which is not from any class: id={}".format(ins.id))

    for child in test_package.children:
        test_package_parse_inheritance(child, model_package)


def package_sort_classes(package):
    # print(f"SORT {package.name}")
    unordered_list = package.classes
    unordered_composed_list = []
    for cls in unordered_list:
        if cls.composed_of != []:
            unordered_composed_list.append(cls)
            package.classes.remove(cls)
            # print(f"  REMOVE {cls.name}")

    # This is crap, do some propper sorting
    unordered_list = unordered_composed_list
    composed_list = []
    for cls1 in unordered_list:
        for cls2 in cls1.composed_of:
            if cls2 in unordered_composed_list:
                unordered_composed_list.remove(cls2)
                composed_list.append(cls2)

    composed_list += unordered_composed_list
    package.classes += composed_list

    for child in package.children:
        package_sort_classes(child)


def instance_parse(session, package: UMLPackage, tobject: TObject):
    ins = UMLInstance(package, tobject.name, tobject.object_id)

    ins.stereotype = tobject.stereotype
    ins.documentation = tobject.note
    ins.status = tobject.status

    # We need to link this instance to the class it is an instance of
    ins.classification_id = tobject.classifier

    # Create attributes for each item found in the runstate
    run_state = tobject.runstate
    if run_state is not None:
        vars = run_state.split('@ENDVAR;')
        for var in vars:
            if var != '':
                variable, value = (var.split(';')[1:3])
                attr = UMLAttribute(ins, variable.split('=')[1], value.split('=')[1])
                attr.value = value.split('=')[1]
                ins.attributes.append(attr)
    else:
        logger.info(f"No runstate found for UMLInstance {ins.name} | {ins.id}")
    logger.debug(f"Added UMLInstance {ins.name}")
    return ins


def association_parse(session, tconnector: TConnector, package: UMLPackage, source: Union[UMLClass, UMLInstance], dest: Union[UMLClass, UMLInstance]):
    association = UMLAssociation(package, source, dest, tconnector.connector_id)
    association.documentation = tconnector.notes

    if tconnector.connector_type == "Aggregation":
        if tconnector.subtype == "Strong":
            association.association_type = UMLAssociationType.COMPOSITION
            if isinstance(dest, UMLClass) and isinstance(source, UMLClass):
                dest.composed_of.append(source)
        else:
            association.association_type = UMLAssociationType.AGGREGATION

    association.source_multiplicity = association.string_to_multiplicity(tconnector.sourcecard)
    association.destination_multiplicity = association.string_to_multiplicity(tconnector.destcard)

    # Use opposing ends class name as attribute name for association
    association.source_name = association.source.name.lower()
    association.destination_name = association.destination.name.lower()

    # If it's an association to or from a multiple then pluralize the name
    if association.destination_multiplicity[1] == '*':
        association.destination_name += 's'
    if association.source_multiplicity[1] == '*':
        association.source_name += 's'

    # Allow explicit naming
    if tconnector.sourcerole is not None:
        association.source_name = tconnector.sourcerole
    if tconnector.destrole is not None:
        association.destination_name = tconnector.destrole

    # Stereotypes
    # TODO: Extract list of stereotypes
    if tconnector.stereotype is not None:
        association.stereotypes = [tconnector.stereotype,]
    if tconnector.sourcestereotype is not None:
        association.source_stereotypes = [tconnector.sourcestereotype,]
    if tconnector.deststereotype is not None:
        association.destination_stereotypes = [tconnector.deststereotype,]

    logging.debug(f"Created {association.cardinality.name} {association.association_type.name} from {association.source_name} to {association.destination_name}")
    return association


def get_stereotypes( session, guid: str ) -> List[str]:
    # TXref
    #   description @STEREO;Name=notifiable;GUID={ADC4E914-13DD-4f1b-A9DB-EDCB89896228};@ENDSTEREO;@STEREO;Name=auditable;GUID={C5DA655B-B862-4a27-96F8-FEB0B2EDD529};@ENDSTEREO;
    stmt = sqlalchemy.select(TXref).where(TXref.client == guid, TXref.name == "Stereotypes")
    txref = session.execute(stmt).scalars().first()
    if txref is not None:
        return re.findall('@STEREO;Name=(.*?);', txref.description)
    else:
        return []


def enumeration_parse(session, package: UMLPackage, tobject: TObject):
    enumeration = UMLEnumeration(package, tobject.name, tobject.object_id)

    # Loop through class elements children for values.
    stmt = sqlalchemy.select(TAttribute).where(TAttribute.object_id == tobject.object_id)
    for tattribute in session.execute(stmt).scalars().all():
        enumeration.values.append(tattribute.name)

    logging.debug(f"Added UMLEnumeration {enumeration.id}:{enumeration.name}")
    return enumeration


def class_parse(session, package: UMLPackage, tobject: TObject):
    cls: UMLClass = UMLClass(package, tobject.name, tobject.object_id)
    if tobject.abstract == '1':
        cls.is_abstract = True
    else:
        cls.is_abstract = False

    cls.alias = tobject.alias
    cls.status = tobject.status
    cls.phase = tobject.phase
    if tobject.note is not None:
        cls.documentation = tobject.note
    else:
        cls.documentation = ""

    # TXref
    #   description @STEREO;Name=notifiable;GUID={ADC4E914-13DD-4f1b-A9DB-EDCB89896228};@ENDSTEREO;@STEREO;Name=auditable;GUID={C5DA655B-B862-4a27-96F8-FEB0B2EDD529};@ENDSTEREO;
    # stmt = sqlalchemy.select(TXref).where(TXref.client == tobject.ea_guid, TXref.name == "Stereotypes")
    # txref = session.execute(stmt).scalars().first()
    # if txref is not None:
    #     cls.stereotypes = re.findall('@STEREO;Name=(.*?);', txref.description)
    cls.stereotypes = get_stereotypes(session, tobject.ea_guid)

    logger.debug(f"Added UMLClass {cls.package.path}{cls.name} | Stereotypes: {cls.stereotypes}")

    stmt = sqlalchemy.select(TAttribute).where(TAttribute.object_id == tobject.object_id)
    for tattribute in session.execute(stmt).scalars().all():
        attr = attr_parse(session, cls, tattribute)
        cls.attributes.append(attr)

    return cls


def attr_parse(session, parent: UMLClass, tattribute: TAttribute):
    attr = UMLAttribute(parent, tattribute.name, tattribute.id)

    # attr.visibility = element.get('visibility')

    type_elem = tattribute.type
    if type_elem is not None:
        attr.set_type(type_elem)
    else:
        logging.error(f"Attribute {attr.name} of class {parent} does not have a type")

    if tattribute.classifier is not None and tattribute.classifier != "0":
        attr.classification_id = tattribute.classifier

    if tattribute.notes is not None:
        attr.documentation = tattribute.notes
    else:
        attr.documentation = ""

    # @PROP=@NAME=isID@ENDNAME;@TYPE=Boolean@ENDTYPE;@VALU=1@ENDVALU;@PRMT=@ENDPRMT;@ENDPROP;
    stmt = sqlalchemy.select(TXref).where(TXref.client == tattribute.ea_guid, TXref.name == "CustomProperties")
    txref = session.execute(stmt).scalars().first()
    if txref is not None:
        attr.is_id = bool(re.findall('@NAME=isID.*@VALU=1(.*?)@ENDVALU;', txref.description))
        if attr.is_id and isinstance(attr.parent, UMLClass):
            attr.parent.id_attribute = attr
    else:
        attr.is_id = False

    # @STEREO;Name=routable;GUID={FCE54E6B-5A61-4336-88FD-7FEF375BB7E1};@ENDSTEREO;
    # stmt = sqlalchemy.select(TXref).where(TXref.client == tattribute.ea_guid, TXref.name == "Stereotypes")
    # txref = session.execute(stmt).scalars().first()
    # if txref is not None:
    #     attr.stereotypes = re.findall('@STEREO;Name=(.*?);', txref.description)
    attr.stereotypes = get_stereotypes(session, tattribute.ea_guid)

    stmt = sqlalchemy.select(TAttributeconstraint).where(TAttributeconstraint.id == tattribute.id)
    for constraint in session.execute(stmt).scalars().all():
        if constraint.Constraint == 'unique':
            attr.is_unique = True
        elif constraint.Constraint.startswith('length'):
            attr.length = int(constraint.Constraint.split("=")[1])

    stmt = sqlalchemy.select(TAttributetag).where(TAttributetag.elementid == tattribute.id )
    for tag in session.execute(stmt).scalars().all():
        attr.tags[tag.property] = tag.value

    logger.debug(f"Added Attribute {attr.parent.name}/{attr.name}")

    return attr
