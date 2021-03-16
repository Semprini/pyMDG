#!/usr/bin/python
from __future__ import annotations
from typing import List, Union, Optional, Any, Tuple
from enum import Enum

from mdg import generation_fields
from mdg.config import settings


class UMLStatuses(Enum):
    Proposed = 1
    Approved = 2
    Implemented = 3
    Mandatory = 4
    Validated = 5


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
        self.status: Optional[UMLStatuses] = None

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
        self.status: Optional[UMLStatuses] = None

    def __str__(self) -> str:
        return f"{self.name}"


class UMLAssociationType(Enum):
    ASSOCIATION = 1
    COMPOSITION = 2
    AGGREGATION = 3


class Cardinality(Enum):
    MANY_TO_ONE = 1
    ONE_TO_MANY = 2
    MANY_TO_MANY = 3
    ONE_TO_ONE = 4


class UMLAssociation(object):
    def __init__(self, package: UMLPackage, source: Union[UMLClass, UMLInstance], destination: Union[UMLClass, UMLInstance], id: Union[int, str], assoc_type=UMLAssociationType.ASSOCIATION):
        self.package: UMLPackage = package

        self.association_type: UMLAssociationType = assoc_type
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
    def cardinality(self):
        cardinality = None
        # Use multiplicities to calculate the CARDINALITY of THYE association
        if self.source_multiplicity[1] == '*' and self.destination_multiplicity[1] in ('0', '1'):
            cardinality = Cardinality.MANY_TO_ONE
        elif self.destination_multiplicity[1] == '*' and self.source_multiplicity[1] in ('0', '1'):
            cardinality = Cardinality.ONE_TO_MANY
        elif self.destination_multiplicity[1] == '*' and self.source_multiplicity[1] == '*':
            cardinality = Cardinality.MANY_TO_MANY
        elif self.destination_multiplicity[1] in ('0', '1') and self.source_multiplicity[1] in ('0', '1'):
            cardinality = Cardinality.ONE_TO_ONE

        return cardinality

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
        elif value == "*..1":
            output = ("*", "1")
        elif value == "*..0":
            output = ("*", "0")

        return output


class UMLEnumeration(object):
    def __init__(self, package: UMLPackage, name: str, id: Union[int, str]):
        self.values: List[str] = []
        self.package: UMLPackage = package
        self.name: str = name
        self.id: Union[int, str] = id
        self.documentation: str = ""
        self.status: Optional[UMLStatuses] = None

    def __str__(self) -> str:
        return f"{self.name}"


class UMLClass(object):
    def __init__(self, package: UMLPackage, name: str, id: Union[int, str]):
        self.name: str = name
        self.alias: Optional[str] = None
        self.id: Union[int, str] = id
        self.attributes: List[UMLAttribute] = []
        self.associations_from: List[UMLAssociation] = []
        self.associations_to: List[UMLAssociation] = []
        self.package: UMLPackage = package
        self.generalization: Optional[UMLClass] = None
        self.generalization_id: Union[None, int, str] = None
        self.specialized_by: List[UMLClass] = []
        self.stereotypes: List[str] = []
        self.id_attribute: Optional[UMLAttribute] = None
        self.documentation: str = ""
        self.is_abstract: bool = False
        self.status: Optional[UMLStatuses] = None

        for inherited_stereotype, inherited_package in package.inherited_stereotypes:
            if not hasattr(self, inherited_stereotype):
                setattr(self, inherited_stereotype, inherited_package)

    def __str__(self) -> str:
        return f"{self.name}"

    def get_name(self) -> str:
        if self.alias and settings['use_alias']:
            return f"{self.alias}"
        else:
            return f"{self.name}"


class UMLAttribute(object):
    def __init__(self, parent: UMLClass, name: str, id: Union[int, str]):
        self.parent: UMLClass = parent
        self.name: str = name
        self.alias: Optional[str] = None
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
        self.scale: Optional[int] = None
        self.precision: Optional[int] = None
        self.validations: List[str] = []

    def __str__(self) -> str:
        return f"{self.name}"

    def get_type(self, translator: Optional[str] = None) -> str:
        if not translator:
            return f"{self.dest_type}"
        if self.type in generation_fields[translator].keys():
            return generation_fields[translator][f"{self.type}"]
        return f"{self.type}"

    def set_type(self, source_type: str):
        # Allow setting of length or scale and precision either: <type> (<precision>,<scale>) or <type> (<length>)
        split: List[str] = source_type.split('(')
        if len(split) > 1:
            source_type = split[0].strip()
            split[1] = split[1].replace(')', '')
            attrs = split[1].split(',')
            if len(attrs) == 1:
                self.length = int(attrs[0])
            elif len(attrs) == 2:
                self.precision = int(attrs[0])
                self.scale = int(attrs[1])
        elif source_type.lower() in ['string', 'str']:
            self.length = 100

        self.type = source_type
        if source_type in generation_fields[settings['generation_type']].keys():
            self.dest_type = generation_fields[settings['generation_type']][source_type]
        else:
            self.dest_type = source_type

    def get_name(self) -> str:
        if self.alias and settings['use_alias']:
            return f"{self.alias}"
        else:
            return f"{self.name}"
