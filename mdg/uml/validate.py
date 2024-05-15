#!/usr/bin/python
from mdg.parse import parse


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
        if cls.id_attribute is None and cls.generalization is None and not cls.is_abstract:
            errors.append(ClassValidationError(package, cls, "no primary key"))
        elif cls.generalization is not None:
            if cls.generalization.id_attribute is not None and cls.generalization.id_attribute != cls.id_attribute:
                errors.append(ClassValidationError(package, cls, "primary key in both class and generalization class"))

        for attr in cls.attributes:
            if "auto" in attr.stereotypes and attr.type not in ("int", "bigint"):
                errors.append(AttributeValidationError(package, cls, attr, "auto increment field must be int or bigint"))

    for child in package.children:
        errors += validate_package(child)

    return errors


def validate():
    """ Loads XMI file from settings as an etree
        Calls XMI parser to turn model and tests into python native (see UML metamodel)
        Calls output functions to render for model and tests
    """

    model_package, test_cases = parse()

    errors = validate_package(model_package)
    if len(errors) > 0:
        print("Validation Errors:")
        for error in errors:
            print("    {}".format(error))

    return errors
