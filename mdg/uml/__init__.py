#!/usr/bin/python
import re


class UMLPackage(object):
    def __init__(self, id, name, parent=None, stereotype=None):
        self.classes = []
        self.associations = []
        self.children = []
        self.instances = []
        self.enumerations = []
        self.parent = parent
        self.stereotype = stereotype
        self.inherited_stereotypes = []
        self.name = name
        self.id = id
        self.diagrams = []
        self.documentation = ""

        if self.parent is None:
            self.root_package = self
            self.path = '/' + self.name + '/'
        else:
            self.root_package = parent.root_package
            self.inherited_stereotypes += parent.inherited_stereotypes
            self.path = self.parent.path + self.name + '/'

    def __str__(self):
        return f"{self.name}"

    def find_by_id(self, id):
        """ Finds UMLPackage, UMLClass, UMLEnumeration or UMLInstance object with specified Id
        Looks for classes part of this package and all sub-packages
        """
        if self.id == id:
            return self

        for cls in self.classes:
            if cls.id == id:
                return cls

        for ins in self.instances:
            if ins.id == id:
                return ins

        for enum in self.enumerations:
            if enum.id == id:
                return enum

        for child in self.children:
            res = child.find_by_id(id)
            if res is not None:
                return res


class UMLInstance(object):
    def __init__(self, package, name, id):
        self.attributes = []
        self.associations_from = []
        self.associations_to = []
        self.package = package
        self.stereotype = None
        self.name = name
        self.id = id
        self.documentation = ""


class UMLAssociation(object):
    def __init__(self, package, source, destination):
        self.package = package
        self.association_type = None

        self.source = source
        self.source_name = None
        self.source_multiplicity = ['0', '0']
        source.associations_from.append(self)

        self.destination = destination
        self.destination_multiplicity = ['0', '0']
        self.destination_name = None
        destination.associations_to.append(self)
        self.documentation = ""

    @property
    def source_name_camel(self):
        return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), self.source_name)

    @property
    def destination_name_camel(self):
        return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), self.destination_name)


class UMLEnumeration(object):
    def __init__(self, package, name, id):
        self.values = []
        self.package = package
        self.name = name
        self.id = id
        self.documentation = ""

    def __str__(self):
        return f"{self.name}"


class UMLClass(object):
    def __init__(self, package, name, id):
        self.name = name
        self.id = id
        self.attributes = []
        self.associations_from = []
        self.associations_to = []
        self.package = package
        self.supertype = None
        self.supertype_id = None
        self.is_supertype = False
        self.stereotypes = []
        self.id_attribute = None
        self.documentation = ""

        for inherited_stereotype, inherited_package in package.inherited_stereotypes:
            if not hasattr(self, inherited_stereotype):
                setattr(self, inherited_stereotype, inherited_package)


class UMLAttribute(object):
    def __init__(self, parent, name, id):
        self.parent = parent
        self.name = name
        self.id = id
        self.is_unique = False
        self.stereotype = None
        self.classification = None
        self.classification_id = None
        self.documentation = ""
        self.dest_type = None
        self.value = None

    def name_camel(self):
        return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), self.name)
