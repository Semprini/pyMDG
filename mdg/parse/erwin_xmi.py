# import re
from typing import List, Tuple, Union
from lxml import etree
import logging
# from decimal import Decimal

from mdg.config import settings
from mdg.uml import (
    UMLAssociation,
    UMLAttribute,
    UMLClass,
    UMLComponent,
    UMLEnumeration,
    UMLInstance,
    UMLPackage,
    # UMLAssociationType,
)


logger = logging.getLogger(__name__)


def parse_uml() -> Tuple[UMLPackage, List[UMLInstance]]:
    """ Root package parser entry point.
    """
    test_cases: List[UMLInstance] = []

    # Parse into etree and grab root package
    logger.debug(f"loading etree from {settings['source']}")
    tree = etree.parse(settings['source'])
    root_package = tree.find('XMI.content')

    # Find the element that is the root for models
    logger.info("Parsing models")
    model_element = root_package.xpath("//Model_Management.Package[@xmi.id='%s']" % settings['model_package'])
    if len(model_element) == 0:
        raise ValueError("Model package element not found. Settings has:{}".format(settings['model_package']))
    model_element = model_element[0]

    # Create our root model UMLPackage and parse in 3 passes
    model_package = package_parse(model_element, root_package, None)
    # logger.debug("Parsing inheritance")
    # model_package_parse_inheritance(model_package)
    logger.debug("Parsing associations")
    package_parse_associations(model_package, model_element)
    # logger.debug("Sorting objects")
    # package_sort_classes(model_package)

    # if 'test_package' in settings.keys():
    #     logger.info("Parsing test cases")

    #     # Find the element that is the root for test data
    #     test_element = element.xpath("//packagedElement[@name='%s']" % settings['test_package'], namespaces=ns)
    #     if len(test_element) == 0:
    #         raise ValueError("Test packaged element not found. Settings has:{}".format(settings['test_package']))
    #     test_element = test_element[0]

    #     # Create our root test data UMLPackage and parse in 2 passes. Does not support inheritance
    #     e_type = test_element.get('{%s}type' % ns['xmi'])
    #     if e_type == 'uml:Package':
    #         test_package = package_parse(test_element, tree, None)
    #         package_parse_associations(test_package, test_element, test_element)
    #         logger.debug("Parsing inheritance")
    #         test_package_parse_inheritance(test_package, model_package)

    #         # With our test package parsed, we must return a list of instances instead of hierarchy of packages
    #         test_cases = parse_test_cases(test_package)
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


def package_parse(element, root_element, parent_package):
    """ Extract package details, call class parser for classes and self parser for sub-packages.
    Associations are not done here, but in a 2nd pass using the parse_associations function.
    :param element:
    :param root_element:
    :return:
    :rtype: UMLPackage
    """
    id = element.get('xmi.id')
    name = element.find('Foundation.Core.ModelElement.name').text
    package = UMLPackage(id, name, parent_package)
    package._element = element
    package._root_element = root_element

    # package.documentation = properties.get('documentation')
    # if package.documentation is None:
    #     package.documentation = ""

    # project = detail.find('project')
    # package.status = project.get('status')

    # diagram_elements = root_element.xpath("//diagrams/diagram/model[@package='%s']" % package.id)
    # for diagram_model in diagram_elements:
    #     diagram = diagram_model.getparent()
    #     package.diagrams.append(diagram.get('{%s}id' % ns['xmi']))

    logger.debug("Added UMLPackage {}".format(package.path))
    owned = element.find('Foundation.Core.Namespace.ownedElement')
    package_parse_children(owned, package)
    return package


def package_parse_children(element, package):

    # Loop through all child elements and create nodes for classes and sub packages
    for child in element:
        e_type = child.tag

        if e_type == 'Model_Management.Package':
            pkg = package_parse(child, package._root_element, package)
            package.children.append(pkg)

        elif e_type == 'Foundation.Core.Class':
            cls = class_parse(package, child)
            if cls.name is not None:
                package.classes.append(cls)

#         elif e_type == 'uml:Enumeration':
#             enumeration = enumeration_parse(package, child)
#             if enumeration.name is not None:
#                 package.enumerations.append(enumeration)
#             # print(f"Enum: {package.path}{enumeration}")


def package_parse_associations(package, element):
    """ Packages and classes should already have been parsed so now we link classes for each association.
    This gets messy as XMI output varies based on association type.
    This supports both un-specified and source to destination directional associations
    :param root_element:
    :param element: XML Element
    :type package: UMLPackage
    """
    owned = element.find('Foundation.Core.Namespace.ownedElement')
    for child in owned:
        e_type = child.tag

        if e_type == 'uml:Package':
            pkg = package_parse_associations(package, child)
            package.children.append(pkg)

        if e_type == 'Foundation.Core.Association':
            association = association_parse(package, child)
            package.associations.append(association)


def association_parse(package, element):
    id = element.get('xmi.id')

    ends = element.find('Foundation.Core.Association.connection')
    if len(ends) != 2:
        logger.warn("Two ends of association not provided with id {id}")
        return None
    source_id = ends[0].find("Foundation.Core.AssociationEnd.type")[0].get('xmi.idref')
    dest_id = ends[1].find("Foundation.Core.AssociationEnd.type")[0].get('xmi.idref')

    source = package.root_package.find_by_id(source_id)
    dest = package.root_package.find_by_id(dest_id)

    association = UMLAssociation(package, source, dest, id)

    # Extract multiplicity for source
    multi = ends[0].find('Foundation.Core.AssociationEnd.multiplicity')[0][0][0]
    source_lower = multi.find('Foundation.Data_Types.MultiplicityRange.lower').text
    if source_lower == '-1':
        source_lower = '*'
    source_upper = multi.find('Foundation.Data_Types.MultiplicityRange.upper').text
    if source_upper == '-1':
        source_upper = '*'
    association.source_multiplicity = (source_lower, source_upper)

    # Extract multiplicity for dest
    multi = ends[1].find('Foundation.Core.AssociationEnd.multiplicity')[0][0][0]
    dest_lower = multi.find('Foundation.Data_Types.MultiplicityRange.lower').text
    if dest_lower == '-1':
        dest_lower = '*'
    dest_upper = multi.find('Foundation.Data_Types.MultiplicityRange.upper').text
    if dest_upper == '-1':
        dest_upper = '*'
    association.destination_multiplicity = (dest_lower, dest_upper)

    print(f"{source_id} to {dest_id} | {source_lower} | {source_upper} | {dest_lower} | {dest_upper} | {association.cardinality}")

#     assoc_type = source_element.get("aggregation")
#     if assoc_type == "composite":
#         association.association_type = UMLAssociationType.COMPOSITION
#         dest.composed_of.append(source)
#     elif assoc_type == "shared":
#         association.association_type = UMLAssociationType.AGGREGATION

#     # If it's an association to or from a multiple then pluralize the name
#     # TODO: Allow pluralized name to be specified in UML
#     # Use opposing ends class name as attribute name for association
    association.destination_name = association.destination.name.lower()
    if association.destination_multiplicity[1] == '*':
        association.destination_name += 's'
    association.source_name = association.source.name.lower()
    if association.source_multiplicity[1] == '*':
        association.source_name += 's'

#     # Allow explicit naming
#     if dest_element.get('name') is not None:
#         association.source_name = dest_element.get('name')
#     if source_element.get('name') is not None:
#         association.destination_name = source_element.get('name')

    return association


# def enumeration_parse(package, element):
#     enumeration = UMLEnumeration(package, element.get('name'), element.get('{%s}id' % ns['xmi']))

#     # Loop through class elements children for values.
#     for child in element:
#         e_type = child.get('{%s}type' % ns['xmi'])
#         if e_type == 'uml:EnumerationLiteral':
#             enumeration.values.append(child.get('name'))
#     logger.debug(f"Added UMLEnumeration {enumeration.name}")
#     return enumeration


def class_parse(package, element):
    id = element.get('xmi.id')
    name = element.find('Foundation.Core.ModelElement.name').text
    cls: UMLClass = UMLClass(package, name, id)
    if element.find('Foundation.Core.GeneralizableElement.isAbstract').get('value') == 'true':
        cls.is_abstract = True
    else:
        cls.is_abstract = False

    print(f"Added UMLClass {cls.id}: {cls.name}")

    # Loop through class elements children for attributes.
    features = element.find('Foundation.Core.Classifier.feature')
    if features is not None:
        for child in features:
            e_type = child.tag

            if e_type == 'Foundation.Core.Attribute':
                attr = attr_parse(cls, child)
                cls.attributes.append(attr)

    return cls


def attr_parse(parent: Union[UMLClass, UMLEnumeration, UMLComponent], element):
    id = element.get('xmi.id')
    name = element.find('Foundation.Core.ModelElement.name').text
    attr = UMLAttribute(parent, name, id)

    attr.visibility = element.find('Foundation.Core.ModelElement.visibility').get('xmi.value')
#     type_elem = element.find('type')
#     if type_elem is not None:
#         type_id = type_elem.get('{%s}idref' % ns['xmi'])
#         if type_id[:4] == 'EAID':
#             attr.classification_id = type_id
#     else:
#         logging.error(f"Attribute {attr.name} of class {parent} does not have a type")

#     alias_node = detail.find('style')
#     attr.alias = alias_node.get('value')

#     xrefs = detail.find('xrefs')
#     if xrefs.get('value') is not None and 'NAME=isID' in xrefs.get('value'):
#         attr.is_id = True
#         attr.parent.id_attribute = attr
#     else:
#         attr.is_id = False

    print(f"Added attr {attr.id}: {attr.name}")
    return attr
