#!/usr/bin/python
from __future__ import annotations
import re
from typing import List, Union, Optional, Any


class UMLPackage(object):
    def __init__(self, id: Union[int, str], name: str, parent: Optional[UMLPackage] = None, stereotype: Optional[str] = None):
        self.classes: List[UMLClass] = []
        self.associations: List[UMLAssociation] = []
        self.children: List[UMLPackage] = []
        self.instances: List[UMLInstance] = []
        self.enumerations: List[UMLEnumeration] = []
        self.parent: Optional[UMLPackage] = parent
        self.stereotype: Optional[str] = stereotype
        self.inherited_stereotypes: List[str] = []
        self.name: str = name
        self.id: Union[int, str] = id
        self.diagrams: Any = []
        self.documentation: str = ""
        self.element: Any = None
        self.root_element: Any = None

        if self.parent is None:
            self.root_package: UMLPackage = self
            self.path = '/' + self.name + '/'
        else:
            self.root_package = self.parent.root_package
            self.inherited_stereotypes += self.parent.inherited_stereotypes
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

    def add_child(self, id: Union[int, str], name: str, stereotype=None) -> UMLPackage:
        package = UMLPackage(id, name, self, stereotype)
        self.children.append(package)
        return package


class UMLInstance(object):
    def __init__(self, package: UMLPackage, name: str, id: Union[int, str]):
        self.attributes: List[UMLAttribute] = []
        self.associations_from: List[UMLInstance] = []
        self.associations_to: List[UMLInstance] = []
        self.package = package
        self.stereotype = None
        self.name = name
        self.id = id
        self.documentation = ""

    def __str__(self) -> str:
        return f"{self.name}"


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

    def __str__(self) -> str:
        return f"{self.source_name} -> {self.destination_name}"


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
        self.is_abstract = False

        for inherited_stereotype, inherited_package in package.inherited_stereotypes:
            if not hasattr(self, inherited_stereotype):
                setattr(self, inherited_stereotype, inherited_package)

    def __str__(self):
        return f"{self.name}"


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
        self.type = None
        self.dest_type = None
        self.value = None
        self.visibility = True
        self.is_id = False
        self.length = 0

    def name_camel(self):
        return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), self.name)

    def __str__(self):
        return f"{self.name}"
