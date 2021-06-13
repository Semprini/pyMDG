from typing import get_type_hints
from mdg.uml import UMLPackage, UMLClass, UMLAssociation, UMLEnumeration, UMLAttribute

schema: dict = {}

schema['UMLPackage'] = get_type_hints(UMLPackage)
schema['UMLClass'] = get_type_hints(UMLClass)
schema['UMLAssociation'] = get_type_hints(UMLAssociation)
schema['UMLEnumeration'] = get_type_hints(UMLEnumeration)
schema['UMLAttribute'] = get_type_hints(UMLAttribute)

print(schema)
