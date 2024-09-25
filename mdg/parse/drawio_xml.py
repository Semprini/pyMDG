from typing import List, Tuple, Optional
from lxml import etree, html
import logging

from mdg.config import settings
from mdg.uml import (
    UMLAssociation,
    UMLAssociationType,
    UMLAttribute,
    UMLClass,
    UMLEnumeration,
    UMLInstance,
    UMLPackage,
)


logger = logging.getLogger(__name__)


def get_label_name(element) -> Optional[str]:
    label_element = element.get("label")
    if label_element == "":
        return None
    tree = html.fromstring(label_element)
    label = "".join(list(tree.itertext()))
    return label


def find_label_name(element, name):
    objects = element.findall('object')

    for object in objects:
        label = get_label_name(object)
        if label and name in label:
            return object
    return None


def parse_uml() -> Tuple[UMLPackage, List[UMLInstance]]:
    test_cases: List[UMLInstance] = []

    # Parse into etree and grab root package
    root = etree.parse(settings['source']).getroot() # type: ignore
    model = root.find('./diagram/mxGraphModel/root')
    if model is None:
        raise ValueError(f"Cannot find model named {settings['source']} in XML at path ./diagram/mxGraphModel/root")

    element = find_label_name(model, settings['root_package'])
    if element is None:
        raise ValueError("Root package element not found. Settings has:{}".format(settings['root_package']))

    model_element = find_label_name(model, settings['model_package'])
    if model_element is None:
        raise ValueError("Model element not found. Settings has:{}".format(settings['model_package']))

    model_package = package_parse(model_element, root, None)
    if model_package is None:
        raise ValueError("Could not parse packages from model element. Settings has:{}".format(settings['model_package']))

    enumeration_link(model_package)

    return model_package, test_cases


def package_parse(element, root_element, parent_package: Optional[UMLPackage]) -> Optional[UMLPackage]:
    """ Extract package details, call class parser for classes and self parser for sub-packages.
    Association linking is not done here, but in a 2nd pass using the parse_associations function.
    """

    name = get_label_name(element)
    id = element.get('id')
    if name is None or id is None:
        logger.warn(f"Could not find valid name of package in XML node 'label'. Node has keys of {element.keys()} and values of {element.values()}")
        return None

    package = UMLPackage(id, name, parent_package)
    package._root_element = root_element

    model = root_element.find('./diagram/mxGraphModel/root')
    child_elements = model.findall('object/mxCell[@parent="{}"]'.format(id))

    logger.debug("Added UMLPackage {}".format(package.path))

    # Parse classes
    for element in child_elements:
        object_element = element.find("..")
        element_type = object_element.get("UMLType")

        if element_type == "Class":
            cls = class_parse(package, object_element, root_element)
            if cls:
                package.classes.append(cls)

        elif element_type == "Enumeration":
            enum = enumeration_parse(package, object_element, root_element)
            if enum:
                package.enumerations.append(enum)

        elif element_type == "Package":
            pkg = package_parse(object_element, package._root_element, package)
            if pkg:
                package.children.append(pkg)

    # Classes are needed to parse generalisations and associations
    for element in child_elements:
        object_element = element.find("..")
        element_type = object_element.get("UMLType")

        if element_type == "Generalization":
            generalization_parse(package, object_element, root_element)
        elif element_type == "Association":
            association_parse(package, object_element, root_element)
        elif element_type == "Composition":
            association_parse(package, object_element, root_element)

    return package


def find_enumeration_by_name(package, name):
    for enum in package.enumerations:
        if enum.name == name:
            return enum
    for child in package.children:
        res = find_enumeration_by_name(child, name)
        if res is not None:
            return res


def enumeration_link(package):
    root_package = package
    while root_package.parent is not None:
        root_package = root_package.parent

    for cls in package.classes:
        for attr in cls.attributes:
            enum = find_enumeration_by_name(root_package, attr.dest_type)
            if enum is not None:
                attr.classification = enum
    for child in package.children:
        enumeration_link(child)


def generalization_parse(package: UMLPackage, element, root):
    cell = element.find("mxCell")
    source: Optional[UMLClass] = package.find_class_by_id(cell.get("source"))
    target: Optional[UMLClass] = package.find_class_by_id(cell.get("target"))
    if source == None or target == None:
        s = cell.get("source")
        t = cell.get("target")
        logger.warn(f"Cannot find generalization class. Source Id:{s}, Target Id: {t}")
    else:
        source.generalization = target
        target.specialized_by.append(source)
        if source.id_attribute is None:
            source.id_attribute = target.id_attribute


def association_parse(package: UMLPackage, element, root):
    id = element.get("id")
    cell = element.find("mxCell")
    source: Optional[UMLClass] = package.find_class_by_id(cell.get("source"))
    target: Optional[UMLClass] = package.find_class_by_id(cell.get("target"))
    element_type = element.get("UMLType")

    if source == None or target == None:
        logger.warn(f"Cannot find association class. Source Id:{cell.get("source")}, Target Id: {cell.get("target")}")
        return
    else:
        association = UMLAssociation(package, source, target, id, UMLAssociationType[element_type.upper()])

    # Extract multiplicities
    ret = root.findall('.//object[@UMLType="DestinationMultiplicity"]')
    for dest in ret:
        dm = dest.find('mxCell[@parent="{}"]'.format(association.id))
        if dm is not None:
            label = dest.get("label").strip('<div>').strip('</div>')
            association.destination_multiplicity = association.string_to_multiplicity(label)
            break
    ret = root.findall('.//object[@UMLType="SourceMultiplicity"]')
    for dest in ret:
        dm = dest.find('mxCell[@parent="{}"]'.format(association.id))
        if dm is not None:
            label = dest.get("label").strip('<div>').strip('</div>')
            association.source_multiplicity = association.string_to_multiplicity(label)
            break

    # Set association destination name
    destination_name = element.get("destination_name")
    if destination_name is not None:
        association.destination_name = destination_name
    else:
        association.destination_name = target.name
        if association.source_multiplicity[1] == '*' and association.association_type == UMLAssociationType.ASSOCIATION:
            association.destination_name += 's'
        elif association.destination_multiplicity[1] == '*' and association.association_type == UMLAssociationType.COMPOSITION:
            association.destination_name += 's'

    # Set association source name
    source_name = element.get("source_name")
    if source_name is not None:
        association.source_name = source_name
    else:
        association.source_name = source.name
        if association.destination_multiplicity[1] == '*' and association.association_type == UMLAssociationType.ASSOCIATION:
            association.source_name += 's'
        if association.source_multiplicity[1] == '*' and association.association_type == UMLAssociationType.COMPOSITION:
            association.source_name += 's'


def class_parse(package: UMLPackage, element, root) -> Optional[UMLClass]:
    stereotypes = []
    label = get_label_name(element)
    if label is None:
        logger.warn(f"Could not find valid name of class in XML node 'label'. Node has keys of {element.keys()} and values of {element.values()}")
        return None
    label_split = label.split(">>")
    if len(label_split) > 1:
        name = label[-1]
        stereotypes = label[0].split(',')
    else:
        name = label

    id = element.get("id")
    cls = UMLClass(package, name, id)
    for stereotype in stereotypes:
        cls.stereotypes.append(stereotype.strip())

    abstract = element.get("Abstract")
    if abstract is not None and abstract == "True":
        cls.is_abstract = True

    logger.debug("Added UMLClass {}".format(cls.name))

    children = root.findall('./diagram/mxGraphModel/root/mxCell[@parent="{}"]'.format(id))
    # Grab a list of the attribute stereotypes and their heights
    stereotypes = []
    for child in children:
        value = child.get("value")
        if "<<" in value:
            geometry = child.find("mxGeometry")
            stereotypes.append((value.strip("<<").strip(">>"), int(geometry.get("y"))))

    # Create all the attributes
    for child in children:
        value = child.get("value")
        if value[0:2] != "<<":
            attr = attr_parse(cls, child, root, stereotypes)
            cls.attributes.append(attr)

    return cls


def enumeration_parse(package: UMLPackage, element, root) -> Optional[UMLEnumeration]:
    label = get_label_name(element)
    if label is None:
        logger.warn(f"Could not find valid name of enumeration in XML node 'label'. Node has keys of {element.keys()} and values of {element.values()}")
        return None
    label_split = label.split(">>")
    if len(label_split) > 1:
        name = label[-1]
    else:
        name = label

    id = element.get("id")
    enum = UMLEnumeration(package, name, id)

    children = root.findall('./diagram/mxGraphModel/root/mxCell[@parent="{}"]'.format(id))
    for child in children:
        enum.values.append(child.get('value'))

    logger.debug("Added UMLEnumeration {}".format(enum.name))

    return enum


def attr_parse(parent: UMLClass, element, root, stereotypes) -> UMLAttribute:
    value = element.get("value").strip("<div>").strip("</div>").strip("<br")
    # height = int(element.find("mxGeometry").get("y"))

    dq = []
    if "{dq_even}" in value:
        dq.append('even')
        value = value.replace("{dq_even}", "").strip()

    is_id = False
    if "{id}" in value:
        is_id = True
        value = value.replace("{id}", "").strip()

    visibility: bool = False
    if value.startswith("+"):
        visibility = True
    value = value.strip("+").strip("-").strip()

    name, attr_type = value.split(":")

    attr = UMLAttribute(parent, name, element.get('id'))
    if is_id:
        attr.is_id = is_id
        parent.id_attribute = attr
    attr.visibility = visibility

    attr.validations = dq

    attr.set_type(attr_type.strip())

    return attr
