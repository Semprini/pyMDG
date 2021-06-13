from typing import get_type_hints, Any
import json
from enum import Enum
# from json import JSONEncoder
from . import UMLPackage

DEFAULT_TYPES = [str, list, dict, bool, int, type(None)]


def obj_to_dict(obj: Any, base_dict={}) -> dict:
    output = {}
    for attr_name in get_type_hints(type(obj)).keys():
        if hasattr(obj, attr_name):
            value = getattr(obj, attr_name)
            if type(value) not in DEFAULT_TYPES and not isinstance(value, Enum):
                if attr_name in obj.Meta.owned_subobjects:
                    value = obj_to_dict(value)
                else:
                    value = getattr(value, value.Meta.id_field)
            elif type(value) == list:
                new_value: Any = []
                for element in value:
                    if type(element) not in DEFAULT_TYPES and not isinstance(element, Enum):
                        if attr_name in obj.Meta.owned_subobjects:
                            new_value.append(obj_to_dict(element))
                        else:
                            new_value.append(getattr(element, element.Meta.id_field))
                    else:
                        new_value.append(element)
                value = new_value
            output[attr_name] = value
    return output


def dumps(package: UMLPackage) -> str:
    output = obj_to_dict(package)

    print(json.dumps(output))

    return f"{output}"


# def load(filename: str) -> UMLPackage:
#     package: UMLPackage = None
#     with open(filename) as file:
#         data = json.load(file)

#     return package
