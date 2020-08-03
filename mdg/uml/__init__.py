#!/usr/bin/python
from __future__ import annotations
from typing import List, Union, Optional, Any, Tuple

from mdg.config import settings


class UMLPackage(object):
    def __init__(self, id: Union[int, str], name: str, parent: Optional[UMLPackage] = None, stereotype: Optional[str] = None):
        self.classes: List[UMLClass] = []
        self.associations: List[UMLAssociation] = []
        self.children: List[UMLPackage] = []
        self.instances: List[UMLInstance] = []
        self.enumerations: List[UMLEnumeration] = []
        self.parent: Optional[UMLPackage] = parent
        self.stereotype: Optional[str] = stereotype
        self.inherited_stereotypes: List[Tuple[str, UMLPackage]] = []
        self.name: str = name
        self.id: Union[int, str] = id
        self.diagrams: Any = []
        self.documentation: str = ""
        self.element: Any = None
        self.root_element: Any = None

        if self.parent is None:
            self.root_package: UMLPackage = self
            self.path = '/' + settings['root_package'] + '/'
        else:
            self.root_package = self.parent.root_package
            self.inherited_stereotypes += self.parent.inherited_stereotypes
            self.path = self.parent.path + self.name + '/'

    def __str__(self):
        return f"{self.name}"

    def find_by_id(self, id: Union[int, str]):
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
        package: UMLPackage = UMLPackage(id, name, self, stereotype)
        self.children.append(package)
        return package


class UMLInstance(object):
    def __init__(self, package: UMLPackage, name: str, id: Union[int, str]):
        self.attributes: List[UMLAttribute] = []
        self.associations_from: List[UMLAssociation] = []
        self.associations_to: List[UMLAssociation] = []
        self.package: UMLPackage = package
        self.stereotype: Optional[str] = None
        self.name: str = name
        self.id: Union[int, str] = id
        self.documentation: str = ""

    def __str__(self) -> str:
        return f"{self.name}"


class UMLAssociation(object):
    def __init__(self, package: UMLPackage, source: Union[UMLClass, UMLInstance], destination: Union[UMLClass, UMLInstance], id):
        self.package: UMLPackage = package

        self.source: Union[UMLClass, UMLInstance] = source
        self.source_name: Optional[str] = None
        self.source_multiplicity: Tuple[str, str] = ('0', '0')
        source.associations_from.append(self)

        self.destination: Union[UMLClass, UMLInstance] = destination
        self.destination_multiplicity: Tuple[str, str] = ('0', '0')
        self.destination_name: Optional[str] = None
        destination.associations_to.append(self)
        self.documentation: str = ""
        self.id: Union[int, str] = id

    def __str__(self) -> str:
        return f"{self.source_name}({self.source_multiplicity}) -> {self.destination_name}({self.destination_multiplicity})"

    @property
    def association_type(self):
        association_type = None
        # Use multiplicities to calculate the type of association
        if self.source_multiplicity[1] == '*' and self.destination_multiplicity[1] in ('0', '1'):
            association_type = 'ManyToOne'
        elif self.destination_multiplicity[1] == '*' and self.source_multiplicity[1] in ('0', '1'):
            association_type = 'OneToMany'
        elif self.destination_multiplicity[1] == '*' and self.source_multiplicity[1] == '*':
            association_type = 'ManyToMany'
        elif self.destination_multiplicity[1] in ('0', '1') and self.source_multiplicity[1] in ('0', '1'):
            association_type = 'OneToOne'

        return association_type

    def string_to_multiplicity(self, value):
        output = ('', '')
        if value == "0..*":
            output = ("0", "*")
        elif value == "1..*":
            output = ("1", "*")
        elif value in ("1", "0..1"):
            output = ("0", "1")
        elif value == "1..1":
            output = ("1", "1")

        return output


class UMLEnumeration(object):
    def __init__(self, package: UMLPackage, name: str, id: Union[int, str]):
        self.values: List[str] = []
        self.package: UMLPackage = package
        self.name: str = name
        self.id: Union[int, str] = id
        self.documentation: str = ""

    def __str__(self) -> str:
        return f"{self.name}"


class UMLClass(object):
    def __init__(self, package: UMLPackage, name: str, id: Union[int, str]):
        self.name: str = name
        self.id: Union[int, str] = id
        self.attributes: List[UMLAttribute] = []
        self.associations_from: List[UMLAssociation] = []
        self.associations_to: List[UMLAssociation] = []
        self.package: UMLPackage = package
        self.supertype: Optional[UMLClass] = None
        self.supertype_id: Union[None, int, str] = None
        self.is_supertype: bool = False
        self.stereotypes: List[str] = []
        self.id_attribute: Optional[UMLAttribute] = None
        self.documentation: str = ""
        self.is_abstract: bool = False

        for inherited_stereotype, inherited_package in package.inherited_stereotypes:
            if not hasattr(self, inherited_stereotype):
                setattr(self, inherited_stereotype, inherited_package)

    def __str__(self) -> str:
        return f"{self.name}"


class UMLAttribute(object):
    def __init__(self, parent: UMLClass, name: str, id: Union[int, str]):
        self.parent: UMLClass = parent
        self.name: str = name
        self.id: Union[int, str] = id
        self.is_unique: bool = False
        self.stereotype: Optional[str] = None
        self.classification: Optional[UMLClass] = None
        self.classification_id: Union[None, int, str] = None
        self.documentation: str = ""
        self.type: Optional[str] = None
        self.dest_type: Optional[str] = None
        self.value: Optional[str] = None
        self.visibility: bool = True
        self.is_id: bool = False
        self.length: int = 0

    def __str__(self) -> str:
        return f"{self.name}"
