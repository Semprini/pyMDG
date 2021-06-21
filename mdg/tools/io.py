from typing import get_type_hints, Any
from enum import Enum

DEFAULT_TYPES = [str, list, dict, bool, int, type(None)]


def obj_to_dict(obj: Any, base_dict={}) -> dict:
    """
from typing import List
from mdg.tools.io import *
class foo:
    z: int
    class Meta:
        id_field = 'z'

class blort:
    b: List[foo]
    c: foo
    class Meta:
        owned_subobjects = 'b'

a = foo()
a.z = 2
b = blort()
b.b = [a,]
b.c = a

obj_to_dict(b)
    """
    # Attributes to convert are specified in object definition type hints
    type_dict: dict = get_type_hints(type(obj))
    output = {}

    # Loop through all type hints on object and convert
    for attr_name in type_dict.keys():
        # Attribute must be set on instance
        if hasattr(obj, attr_name):
            value = getattr(obj, attr_name)

            # If the value is not a base type or enum then it's a class TODO: Actual check for class
            if type(value) not in DEFAULT_TYPES and not isinstance(value, Enum):
                # If the class is owned by this parent class then convert to a dict
                if attr_name in obj.Meta.owned_subobjects:
                    value = obj_to_dict(value)
                # If the class is not owned by this parent class then convert to a reference
                else:
                    value = getattr(value, value.Meta.id_field)

            # If value is a list then examine the type of the list and convert each element
            elif type(value) == list:
                new_value: Any = []
                for element in value:
                    # Check for base types as in non list mode above: TODO: Actual check for class
                    if type(element) not in DEFAULT_TYPES and not isinstance(element, Enum):
                        # Check for class ownership as above
                        if attr_name in obj.Meta.owned_subobjects:
                            new_value.append(obj_to_dict(element))
                        else:
                            new_value.append(getattr(element, element.Meta.id_field))
                    # Just a base type so use the value
                    else:
                        new_value.append(element)
                value = new_value

            # Value has been created so set the dictionary item
            output[attr_name] = value
    return output


def dict_to_obj(input: dict, base_object_class) -> object:
    """
from typing import List
from mdg.uml.io import *
class foo:
    a: int

class blort:
    b: List[foo]

input={'b':[{'a':1}]}
dict_to_obj(input, blort)
    """
    # Instantiate the requested class & get the type hints
    obj = base_object_class()
    type_dict = get_type_hints(type(obj))

    for attr_name in type_dict.keys():
        if attr_name in input.keys():
            # The input has this item defined in the class so extract
            attr_type = type(input[attr_name])  # type_dict[attr_name].__origin__ TODO: use definition rather than input

            if type(input[attr_name]) != list:
                if attr_type in DEFAULT_TYPES:
                    # Value definition is standard type so just set the value
                    setattr(obj, attr_name, input[attr_name])
                elif type(input[attr_name]) == dict:
                    # Not a standard type, must be class so recurse to expand sub-object
                    setattr(obj, attr_name, dict_to_obj(input[attr_name], type_dict[attr_name]))
                else:
                    # TODO: Check Id field
                    # If definition is class and dict value has string then must be a reference using id_field value from Meta
                    pass
            else:
                # Input has a list of something, loop through each element and extract
                value = []
                item_type = type_dict[attr_name].__args__[0]
                for item in input[attr_name]:
                    if item_type in DEFAULT_TYPES:
                        # List of standard type so just add the value
                        value.append(item)
                    else:
                        # attr_class = type_dict[attr_name].__args__[0]
                        if type(item) == dict:
                            # Class definition has list of class instances and input has a dictionary so recurse to expand sub-object
                            item_value = dict_to_obj(item, item_type)
                            value.append(item_value)
                        else:
                            # TODO: Check Id field
                            # If definition is class and dict value has string then must be a reference using id_field value from Meta
                            pass
                setattr(obj, attr_name, value)
    return obj
