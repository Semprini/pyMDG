from typing import List, Tuple, Optional
from lxml import etree
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


def get_label_name(element):
    label = element.get("label")
    label = label.strip("<div>").strip("</div>")
    return label


def find_label_name(element, name):
    objects = element.findall('object')

    for object in objects:
        label = get_label_name(object)
        if name in label:
            return object
    return None


def parse_uml() -> Tuple[UMLPackage, List[UMLInstance]]:
    test_cases: List[UMLInstance] = []

    # Parse into etree and grab root package
    root = etree.parse(settings['source']).getroot()
    model = root.find('./diagram/mxGraphModel/root')
    if model is None:
        raise ValueError("Cannot find model in XML at path ./diagram/mxGraphModel/root")

    element = find_label_name(model, settings['root_package'])
    if element is None:
        raise ValueError("Root package element not found. Settings has:{}".format(settings['root_package']))

    model_element = find_label_name(model, settings['model_package'])
    if model_element is None:
        raise ValueError("Model element not found. Settings has:{}".format(settings['model_package']))

    model_package: UMLPackage = package_parse(model_element, root, None)

    enumeration_link(model_package)

    return model_package, test_cases


def package_parse(element, root_element, parent_package: Optional[UMLPackage]) -> UMLPackage:
    """ Extract package details, call class parser for classes and self parser for sub-packages.
    Association linking is not done here, but in a 2nd pass using the parse_associations function.
    """

    name = get_label_name(element)
    id = element.get('id')

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
            package.classes.append(cls)

        elif element_type == "Enumeration":
            enum = enumeration_parse(package, object_element, root_element)
            package.enumerations.append(enum)

        elif element_type == "Package":
            pkg = package_parse(object_element, package._root_element, package)
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
    source: UMLClass = package.find_by_id(cell.get("source"))
    target: UMLClass = package.find_by_id(cell.get("target"))
    source.generalization = target


def association_parse(package: UMLPackage, element, root):
    id = element.get("id")
    cell = element.find("mxCell")
    source: UMLClass = package.find_by_id(cell.get("source"))
    target: UMLClass = package.find_by_id(cell.get("target"))
    element_type = element.get("UMLType")

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


def class_parse(package: UMLPackage, element, root) -> UMLClass:
    stereotypes = []
    label = element.get("label").split("<div>")
    if len(label) == 1:
        name = label[0].replace("<b>", "").replace("</b>", "").replace("<i>", "").replace("</i>", "").replace('<br>', "").strip()
    else:
        name = label[-1].replace("</div>", "").replace("<b>", "").replace("</b>", "").replace("<i>", "").replace("</i>", "").replace('<br>', "").strip()
        stereotypes = label[-2].split('&lt;&lt;')[-1].split('&gt;&gt;')[0].split(',')

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


def enumeration_parse(package: UMLPackage, element, root) -> UMLEnumeration:
    label = element.get("label").split(",")[-1].split("div>")
    if len(label) == 1:
        name = label[0].strip("<b>").strip("</b>").strip("i>").strip("</i")
    else:
        name = label[-2].strip("<b>").strip("</b></").strip("i>").strip("</i")
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
