#!/usr/bin/python
from __future__ import annotations
from decimal import Decimal
from typing import List, Union, Optional, Any, Tuple
from enum import Enum
import json

from mdg import generation_fields
from mdg.config import settings
from mdg.tools.io import obj_to_dict


class UMLStatuses(Enum):
    Proposed = 1
    Approved = 2
    Implemented = 3
    Mandatory = 4
    Validated = 5


class UMLAssociationType(Enum):
    ASSOCIATION = 1
    COMPOSITION = 2
    AGGREGATION = 3


class Cardinality(Enum):
    MANY_TO_ONE = 1
    ONE_TO_MANY = 2
    MANY_TO_MANY = 3
    ONE_TO_ONE = 4


class UMLPackage:
    classes: List[UMLClass]
    associations: List[UMLAssociation]
    children: List[UMLPackage]
    instances: List[UMLInstance]
    enumerations: List[UMLEnumeration]
    parent: Optional[UMLPackage] = None
    stereotype: Optional[str] = None
    name: str
    id: Union[int, str]
    diagrams: Any
    documentation: str
    status: Optional[UMLStatuses]

    class Meta:
        id_field = 'id'
        owned_subobjects: List = ['classes', 'associations', 'children', 'enumerations']

    def __init__(self, id: Union[int, str], name: str, parent: Optional[UMLPackage] = None, stereotype: Optional[str] = None) -> None:
        self.classes = []
        self.associations = []
        self.children = []
        self.instances = []
        self.enumerations = []
        self.parent = parent
        self.stereotype = stereotype
        self.inherited_stereotypes: List[Tuple[str, UMLPackage]] = []
        self.name = name
        self.id = id
        self.diagrams = []
        self.documentation = ""
        self.status = None

        self._element: Any = None
        self._root_element: Any = None
        self.root_package: UMLPackage
        self.path: str

        if self.parent is None:
            self.root_package = self
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


class UMLInstance:
    package: UMLPackage
    attributes: List[UMLAttribute]
    stereotype: Optional[str]
    name: str
    id: Union[int, str]
    documentation: str
    status: Optional[UMLStatuses]
    associations_from: List[UMLAssociation]
    associations_to: List[UMLAssociation]
    classification: Optional[UMLClass]

    class Meta:
        id_field = 'id'
        owned_subobjects: List = ['attributes', ]

    def __init__(self, package: UMLPackage, name: str, id: Union[int, str]) -> None:
        self.attributes = []
        self.associations_from = []
        self.associations_to = []
        self.package = package
        self.stereotype = None
        self.name = name
        self.id = id
        self.documentation = ""
        self.status = None
        self.classification_id: Union[None, int, str] = None

    def __str__(self) -> str:
        return f"{self.name}"


class UMLAssociation:
    id: Union[int, str]
    documentation: str

    association_type: UMLAssociationType
    source: Union[UMLClass, UMLInstance]
    source_name: Optional[str]
    source_multiplicity: Tuple[str, str]

    destination: Union[UMLClass, UMLInstance]
    destination_multiplicity: Tuple[str, str]
    destination_name: Optional[str]

    class Meta:
        id_field = 'id'
        owned_subobjects: List = []

    def __init__(self, package: UMLPackage, source: Union[UMLClass, UMLInstance], destination: Union[UMLClass, UMLInstance], id: Union[int, str], assoc_type=UMLAssociationType.ASSOCIATION):
        self.package: UMLPackage = package
        self.id = id
        self.documentation = ""

        self.association_type = assoc_type
        self.source = source
        self.source_name = None
        self.source_multiplicity = ('0', '0')
        source.associations_from.append(self)

        self.destination = destination
        self.destination_multiplicity = ('0', '0')
        self.destination_name = None
        destination.associations_to.append(self)

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


class UMLEnumeration:
    values: List[str]
    package: UMLPackage
    name: str
    id: Union[int, str]
    documentation: str
    status: Optional[UMLStatuses]

    class Meta:
        id_field = 'id'
        owned_subobjects: List = []

    def __init__(self, package: UMLPackage, name: str, id: Union[int, str]):
        self.values = []
        self.package = package
        self.name = name
        self.id = id
        self.documentation = ""
        self.status = None

    def __str__(self) -> str:
        return f"{self.name}"


class UMLClass:
    name: str
    alias: Optional[str]
    id: Union[int, str]
    attributes: List[UMLAttribute]
    associations_from: List[UMLAssociation]
    associations_to: List[UMLAssociation]
    package: UMLPackage
    generalization: Optional[UMLClass]
    specialized_by: List[UMLClass]
    stereotypes: List[str]
    documentation: str
    is_abstract: bool
    status: Optional[UMLStatuses]
    composed_of: List[UMLClass]
    phase: Optional[Decimal]

    class Meta:
        id_field = 'id'
        owned_subobjects: List = ['attributes', ]

    def __init__(self, package: UMLPackage, name: str, id: Union[int, str]):
        self.name = name
        self.alias = None
        self.id = id
        self.attributes = []
        self.associations_from = []
        self.associations_to = []
        self.package = package
        self.generalization = None
        self.generalization_id: Union[None, int, str] = None
        self.specialized_by = []
        self.stereotypes = []
        self.id_attribute: Optional[UMLAttribute] = None
        self.documentation = ""
        self.is_abstract = False
        self.status = None
        self.composed_of = []
        self.phase = None

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


class UMLAttribute:
    parent: UMLClass
    name: str
    alias: Optional[str]
    id: Union[int, str]
    is_unique: bool
    stereotype: Optional[str]
    classification: Optional[UMLClass]
    documentation: str
    type: Optional[str]
    value: Optional[str]
    visibility: bool
    is_id: bool
    length: int
    scale: Optional[int]
    precision: Optional[int]
    validations: List[str]

    class Meta:
        id_field = 'id'
        owned_subobjects: List = []

    def __init__(self, parent: UMLClass, name: str, id: Union[int, str]):
        self.parent = parent
        self.name = name
        self.alias = None
        self.id = id
        self.is_unique = False
        self.stereotype = None
        self.classification = None
        self.classification_id: Union[None, int, str] = None
        self.documentation = ""
        self.type = None
        self.dest_type: Optional[str] = None
        self.value = None
        self.visibility = True
        self.is_id = False
        self.length = 0
        self.scale = None
        self.precision = None
        self.validations = []

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


def dumps(package: UMLPackage) -> str:
    output = obj_to_dict(package)
    return json.dumps(output)
