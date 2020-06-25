#!/usr/bin/python
from lxml import etree

from mdg.xmi.parse import ns, parse_uml
from mdg.config import settings


class ClassValidationError(object):
    def __init__(self, package, cls, error):
        self.package = package
        self.error = error
        self.cls = cls

    def __repr__(self):
        return "Class error: {}{} | {}".format(self.package.path, self.cls.name, self.error)


class AttributeValidationError(object):
    def __init__(self, package, cls, attr, error):
        self.package = package
        self.error = error
        self.cls = cls
        self.attr = attr

    def __repr__(self):
        return "Attribute error: {}{}.{} | {}".format(self.package.path, self.cls.name, self.attr.name, self.error)


def validate_package(package):
    errors = []

    for cls in package.classes:
        if cls.id_attribute is None:
            if cls.supertype is None:
                errors.append(ClassValidationError(package, cls, "no primary key"))
        elif cls.supertype is not None:
            if cls.supertype.id_attribute != cls.id_attribute:
                errors.append(ClassValidationError(package, cls, "primary key in both class and supertype"))

        for attr in cls.attributes:
            if attr.stereotype == "auto" and attr.type not in ("int", "bigint"):
                errors.append(AttributeValidationError(package, cls, attr, "auto increment field must be int or bigint"))

    for child in package.children:
        errors += validate_package(child)

    return errors


def validate(recipie_path):
    tree = etree.parse(settings['source'])
    model = tree.find('uml:Model', ns)
    root_package = model.xpath("//packagedElement[@name='%s']" % settings['root_package'], namespaces=ns)
    if len(root_package) == 0:
        print("Root packaged element not found. Settings has:{}".format(settings['root_package']))
        return
    root_package = root_package[0]

    model_package, test_cases = parse_uml(root_package, tree)

    # validations
    # Does each object have a primary key
    # Do objects with primary keys have a parent class which also has a primary key
    # Are all auto increment fields int
    print(validate_package(model_package))

    # Does each class have a domain
    # Are there unexpected attribute types
