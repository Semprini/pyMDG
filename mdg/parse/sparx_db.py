from typing import List, Tuple, Optional
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

    engine = sqlalchemy.create_engine("sqlite:///sample_recipes/sparx/sample.qea", echo=False, future=True)
    with Session(engine) as session:

        # Find the element that is the root for models
        # stmt = sqlalchemy.select(TPackage, TObject).join(TObject, TObject.package_id == TPackage.parent_id).where(TPackage.name == settings['root_package'], TObject.name == settings['root_package'])
        # root_package, root_object = session.execute(stmt).first()
        # root_object.package = root_package
        # print(f"{root_object.object_type}: {root_object.package.name}")

        # Find the package with the model nodes
        # stmt = sqlalchemy.select(TPackage, TObject).join(TObject, TObject.package_id == TPackage.parent_id).where(TPackage.name == "DataModel", TObject.name == "DataModel")  # settings['model_package'], settings['model_package'])
        stmt = sqlalchemy.select(TPackage).where(TPackage.name == "DataModel")  # settings['model_package'], settings['model_package'])
        model_package = session.execute(stmt).scalars().first()
        # model_object.package = model_package
        # print(f"Model Object: {model_object.object_id}: {model_object.name}")

        # Create our root model UMLPackage and parse in 3 passes
        model_package = package_parse(session, model_package, None)
        logger.debug("Parsing inheritance")
        model_package_parse_inheritance(model_package)
        logger.debug("Parsing associations")
        # package_parse_associations(model_package, model_element, model_element)
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

    print("Added UMLPackage {}".format(package.path))

    package_parse_children(session, package)
    return package


def package_parse_children(session, package):
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

        # elif e_type == 'uml:Enumeration':
        #     enumeration = enumeration_parse(package, child)
        #     if enumeration.name is not None:
        #         package.enumerations.append(enumeration)
            # print(f"Enum: {package.path}{enumeration}")


def package_parse_associations(package, element, root_element):
    """ Packages and classes should already have been parsed so now we link classes for each association.
    This gets messy as XMI output varies based on association type.
    This supports both un-specified and source to destination directional associations
    :param root_element:
    :param element: XML Element
    :type package: UMLPackage
    """
    for child in element:
        e_type = child.get('type')
        e_id = child.get('id')

        if e_type == 'uml:Association':
            assoc_source_id = None
            assoc_dest_id = None
            assoc_source_elem = None
            assoc_dest_elem = None

            for assoc in child:
                # If unspecified direction then both source and destination info are child elements within the
                # association
                assoc_type = assoc.get('type')
                assoc_id = assoc.get('id')
                if assoc_id is not None and assoc_type == 'uml:Property' and assoc_id[:8] == 'EAID_src':
                    assoc_source_elem = assoc
                    assoc_source_type_elem = assoc.find('type')
                    assoc_source_id = assoc_source_type_elem.get('idref')
                if assoc_id is not None and assoc_type == 'uml:Property' and assoc_id[:8] == 'EAID_dst':
                    assoc_dest_elem = assoc
                    assoc_dest_type_elem = assoc.find('type')
                    assoc_dest_id = assoc_dest_type_elem.get('idref')

            # If association direction is source to destination then
            # destination class info is found as an ownedAttribute in the source element
            if assoc_dest_id is None:
                for assoc in child:
                    if assoc.tag == 'memberEnd':
                        assoc_idref = assoc.get('idref')
                        if assoc_idref[:8] == 'EAID_dst':
                            try:
                                assoc_dest_elem = \
                                    root_element.xpath("//ownedAttribute[@xmi:id='%s']" % assoc_idref)[0]
                            except IndexError as e:
                                logger.warn("Failed to find member end association destination. Id: {}".format(assoc_idref))
                                raise e
                            assoc_dest_type_elem = assoc_dest_elem.find('type')
                            assoc_dest_id = assoc_dest_type_elem.get('idref')

            # print("association: src id={} dest id={}".format(assoc_source_id,assoc_dest_id))
            # TODO: Raise error if we don't have a source and dest
            source = package.root_package.find_by_id(assoc_source_id)
            dest = package.root_package.find_by_id(assoc_dest_id)
            if source is not None \
                    and dest is not None \
                    and assoc_source_elem is not None \
                    and assoc_dest_elem is not None:
                association = association_parse(package, assoc_source_elem, assoc_dest_elem, source, dest)
                package.associations.append(association)
                logger.debug(f"Created {association.cardinality.name} {association.association_type.name} from {association.source_name} to {association.destination_name}")
            else:
                logger.warn("Unable to create association id={}".format(e_id))

    for package_child in package.children:
        element = element.xpath("//packagedElement[@xmi:id='%s']" % package_child.id)[0]
        package_parse_associations(package_child, element, root_element)


def model_package_parse_inheritance(package):
    """ Looks for classes which are specializations of a supertype and finds the correct object """
    for cls in package.classes:
        if cls.generalization_id is not None:
            cls.generalization = package.root_package.find_by_id(cls.generalization_id)
            if cls.generalization is None:
                logger.warn("Cannot find specialized class id={}".format(cls.generalization_id))
            else:
                cls.generalization.specialized_by.append(cls)
                if cls.id_attribute is None:
                    cls.id_attribute = cls.generalization.id_attribute

        for attr in cls.attributes:
            if attr.classification_id is not None:
                attr.classification = package.root_package.find_by_id(attr.classification_id)
                if attr.classification is None:
                    logger.warn("Cannot find expected classification for {} of attribute {}. Id={}".format(attr.dest_type, attr.name, attr.classification_id))

    for child in package.children:
        model_package_parse_inheritance(child)


def test_package_parse_inheritance(test_package, model_package):
    """ Links instances with the class they are instances of """

    for ins in test_package.instances:
        if ins.classification_id is not None:
            ins.classification = model_package.find_by_id(ins.classification_id)
            if ins.classification is None:
                logger.warn("Cannot find class which instance is from id={}".format(ins.classification_id))
            else:
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
            logger.warn("Instance object which is not from class id={}".format(ins.id))

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


def association_parse(package, source_element, dest_element, source, dest):
    id = source_element.get('id')
    association = UMLAssociation(package, source, dest, id)

    assoc_type = source_element.get("aggregation")
    if assoc_type == "composite":
        association.association_type = UMLAssociationType.COMPOSITION
        dest.composed_of.append(source)
    elif assoc_type == "shared":
        association.association_type = UMLAssociationType.AGGREGATION

    # Extract multiplicity for source
    source_lower = source_element.find('lowerValue')
    if source_lower is not None:
        source_lower = source_lower.get('value')
        if source_lower == '-1':
            source_lower = '*'
        source_upper = source_element.find('upperValue').get('value')
        if source_upper == '-1':
            source_upper = '*'
        association.source_multiplicity = (source_lower, source_upper)

    # Extract multiplicity for dest
    dest_lower = dest_element.find('lowerValue')
    if dest_lower is not None:
        dest_lower = dest_lower.get('value')
        if dest_lower == '-1':
            dest_lower = '*'
        dest_upper = dest_element.find('upperValue').get('value')
        if dest_upper == '-1':
            dest_upper = '*'
        association.destination_multiplicity = (dest_lower, dest_upper)

    # print('{} {} to {}'.format(association.source.name, association.association_type, association.destination.name))

    # If it's an association to or from a multiple then pluralize the name
    # TODO: Allow pluralized name to be specified in UML
    # Use opposing ends class name as attribute name for association
    association.destination_name = association.destination.name.lower()
    if association.destination_multiplicity[1] == '*':
        association.destination_name += 's'
    association.source_name = association.source.name.lower()
    if association.source_multiplicity[1] == '*':
        association.source_name += 's'

    # Allow explicit naming
    if dest_element.get('name') is not None:
        association.source_name = dest_element.get('name')
    if source_element.get('name') is not None:
        association.destination_name = source_element.get('name')

    # print('Assoc in {}: {} to {}: type = {}'.format(self.source.name, self.source_name, self.destination_name,
    # self.association_type) )
    return association


def enumeration_parse(package, element):
    enumeration = UMLEnumeration(package, element.get('name'), element.get('id'))

    # Loop through class elements children for values.
    for child in element:
        e_type = child.get('type')
        if e_type == 'uml:EnumerationLiteral':
            enumeration.values.append(child.get('name'))
    logger.debug(f"Added UMLEnumeration {enumeration.name}")
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
    #   client {24501FBB-962E-493c-8777-C73D79F7F628}
    #   name Stereotypes
    stmt = sqlalchemy.select(TXref).where(TXref.client == tobject.ea_guid, TXref.name == "Stereotypes")
    txref = session.execute(stmt).scalars().first()
    if txref is not None:
        cls.stereotypes = re.findall('@STEREO;Name=(.*?);', txref.description)

    print(f"Added UMLClass {cls.package.path}{cls.name} | Stereotypes: {cls.stereotypes}")

    stmt = sqlalchemy.select(TAttribute).where(TAttribute.object_id == tobject.object_id)
    for tattribute in session.execute(stmt).scalars().all():
        attr = attr_parse(cls, tattribute)
        cls.attributes.append(attr)

    return cls


def attr_parse(parent: UMLClass, tattribute: TAttribute):
    attr = UMLAttribute(parent, tattribute.name, tattribute.id)

    # attr.visibility = element.get('visibility')
    type_elem = tattribute.type
    if type_elem is not None:
        attr.set_type(type_elem)
    else:
        logging.error(f"Attribute {attr.name} of class {parent} does not have a type")

    attr.documentation = tattribute.notes

    # xrefs = detail.find('xrefs')
    # if xrefs.get('value') is not None and 'NAME=isID' in xrefs.get('value'):
    #     attr.is_id = True
    #     attr.parent.id_attribute = attr
    # else:
    #     attr.is_id = False

    attr.stereotype = tattribute.stereotype

    # constraints = detail.find('Constraints')
    # if constraints is not None:
    #     for constraint in constraints:
    #         name = constraint.get('name')
    #         if name == 'unique':
    #             attr.is_unique = True
    #         elif name.startswith('length'):
    #             attr.length = int(name.split("=")[1])

    print(f"Added Attribute {attr.parent.name}/{attr.name}")

    return attr
