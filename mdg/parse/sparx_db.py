# import enum
from typing import List, Tuple, Optional
import logging
import re
# from decimal import Decimal

import sqlalchemy
from sqlalchemy.orm import Session

from mdg.parse.sparx_db_models import (
    TObject,
    TPackage,
    TXref,
    TAttribute,
    TConnector,
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
)


logger = logging.getLogger(__name__)


def parse_uml() -> Tuple[UMLPackage, List[UMLInstance]]:
    """ Root package parser entry point.
    """
    test_cases: List[UMLInstance] = []

    engine = sqlalchemy.create_engine(f"sqlite:///{settings['source']}", echo=False, future=True)
    with Session(engine) as session:

        # Find the element that is the root for models
        # stmt = sqlalchemy.select(TPackage).where(TPackage.name == settings['root_package'])
        # root_package = session.execute(stmt).first()

        # Find the package with the model nodes. Can specify either EA GUID or name
        # If guid make sure value in recipie is quoted - model_package: "{D6D3BF36-E897-4a8b-8CA9-62ADAAD696ED}"
        if settings['model_package'][0] == "{":
            stmt = sqlalchemy.select(TPackage).where(TPackage.ea_guid == settings['model_package'])
        else:
            stmt = sqlalchemy.select(TPackage).where(TPackage.name == settings['model_package'])
        model_package = session.execute(stmt).scalars().first()
        if model_package is None:
            raise ValueError("Model package element not found. Settings has:{}".format(settings['model_package']))
        logger.debug(f"Model Object: {model_package.package_id}: {model_package.name}")

        # Create our root model UMLPackage and parse in 3 passes
        model_package = package_parse(session, model_package, None)
        # logger.debug("Parsing inheritance")
        # model_package_parse_inheritance(model_package)
        logger.debug("Parsing associations")
        package_parse_associations(session, model_package)
        logger.debug("Sorting objects")
        # package_sort_classes(model_package)

    if 'test_package' in settings.keys():
        logger.info("Parsing test cases")

    return model_package, test_cases


def parse_test_cases(package) -> List[UMLInstance]:
    """ Looks through package hierarchy for instances with request or response stereotype
    and returns list of instances.
    :rtype: list<UMLInstance>
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


def package_parse(session, tpackage: TPackage, parent_package: Optional[UMLPackage]):
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

    logger.debug("Added UMLPackage {}".format(package.path))

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

        # elif e_type == 'uml:InstanceSpecification':
        #     ins = instance_parse(package, child, package._root_element)
        #     if ins.name is not None:
        #         package.instances.append(ins)

        elif child_tobject.object_type == 'Enumeration':
            enumeration = enumeration_parse(session, package, child_tobject)
            package.enumerations.append(enumeration)


def package_parse_associations(session, package: UMLPackage):
    """ Packages and classes should already have been parsed so now we link classes for each association.
    """
    for cls in package.classes:
        stmt = sqlalchemy.select(TConnector).where(TConnector.start_object_id == cls.id)

        for connector in session.execute(stmt).scalars().all():
            dest = package.root_package.find_by_id(connector.end_object_id)

            if connector.connector_type in ["Association", "Aggregation"]:
                association = association_parse(session, connector, package, cls, dest)
                if association is not None:
                    package.associations.append(association)

            elif connector.connector_type == "Generalization":
                cls.generalization = dest
                dest.specialized_by.append(cls)
                if cls.id_attribute is None:
                    cls.id_attribute = dest.id_attribute

        for attr in cls.attributes:
            if attr.classification_id is not None:
                attr.classification = package.root_package.find_by_id(attr.classification_id)
                if attr.classification is None:
                    logger.warn("Cannot find expected classification for {} of attribute {}. Id={}".format(attr.dest_type, attr.name, attr.classification_id))

    for package_child in package.children:
        package_parse_associations(session, package_child)


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


def instance_parse(package, source_element, root):
    ins = UMLInstance(package, source_element.get('name'), source_element.get('id'))

    # Detail is sparx specific
    # TODO: Put modelling tool in settings and use tool specific parser here
    detail = root.xpath("//element[@xmi:idref='%s']" % ins.id)[0]
    properties = detail.find('properties')
    ins.stereotype = properties.get('stereotype')
    ins.documentation = properties.get('documentation')
    if ins.documentation is None:
        ins.documentation = ""

    project = detail.find('project')
    ins.status = project.get('status')

    # We need to link this instance to the class it is an instance of
    ins.classification_id = source_element.get('classifier')

    # Create attributes for each item found in the runstate
    # TODO: Change this to using an re
    extended_properties = detail.find('extendedProperties')
    if extended_properties is not None and extended_properties.get('runstate') is not None:
        run_state = extended_properties.get('runstate')
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


def association_parse(session, tconnector: TConnector, package: UMLPackage, source: UMLClass, dest: UMLClass):
    association = UMLAssociation(package, source, dest, tconnector.connector_id)
    association.documentation = tconnector.notes

    if tconnector.connector_type == "Aggregation":
        if tconnector.subtype == "Strong":
            association.association_type = UMLAssociationType.COMPOSITION
            dest.composed_of.append(source)
        else:
            association.association_type = UMLAssociationType.AGGREGATION

    association.source_multiplicity = association.string_to_multiplicity(tconnector.sourcecard)
    association.destination_multiplicity = association.string_to_multiplicity(tconnector.destcard)

    # Use opposing ends class name as attribute name for association
    # If it's an association to or from a multiple then pluralize the name
    association.destination_name = association.destination.name.lower()
    if association.destination_multiplicity[1] == '*':
        association.destination_name += 's'
    association.source_name = association.source.name.lower()
    if association.source_multiplicity[1] == '*':
        association.source_name += 's'

    # Allow explicit naming
    if tconnector.sourcerole is not None:
        association.source_name = tconnector.sourcerole
    if tconnector.destrole is not None:
        association.destination_name = tconnector.destrole

    logging.debug(f"Created {association.cardinality.name} {association.association_type.name} from {association.source_name} to {association.destination_name}")
    return association


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
    cls.documentation = tobject.note
    cls.status = tobject.status
    cls.phase = tobject.phase

    # TXref
    #   description @STEREO;Name=notifiable;GUID={ADC4E914-13DD-4f1b-A9DB-EDCB89896228};@ENDSTEREO;@STEREO;Name=auditable;GUID={C5DA655B-B862-4a27-96F8-FEB0B2EDD529};@ENDSTEREO;
    stmt = sqlalchemy.select(TXref).where(TXref.client == tobject.ea_guid, TXref.name == "Stereotypes")
    txref = session.execute(stmt).scalars().first()
    if txref is not None:
        cls.stereotypes = re.findall('@STEREO;Name=(.*?);', txref.description)

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

    attr.documentation = tattribute.notes

    # @PROP=@NAME=isID@ENDNAME;@TYPE=Boolean@ENDTYPE;@VALU=1@ENDVALU;@PRMT=@ENDPRMT;@ENDPROP;
    stmt = sqlalchemy.select(TXref).where(TXref.client == tattribute.ea_guid, TXref.name == "CustomProperties")
    txref = session.execute(stmt).scalars().first()
    if txref is not None:
        attr.is_id = bool(re.findall('@NAME=isID.*@VALU=(.*?)@ENDVALU;', txref.description))
        attr.parent.id_attribute = attr
    else:
        attr.is_id = False

    attr.stereotype = tattribute.stereotype

    # constraints = detail.find('Constraints')
    # if constraints is not None:
    #     for constraint in constraints:
    #         name = constraint.get('name')
    #         if name == 'unique':
    #             attr.is_unique = True
    #         elif name.startswith('length'):
    #             attr.length = int(name.split("=")[1])

    logger.debug(f"Added Attribute {attr.parent.name}/{attr.name}")

    return attr
