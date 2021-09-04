from typing import get_type_hints, Any, Tuple
from enum import Enum

DEFAULT_TYPES = [str, list, tuple, dict, bool, int, type(None)]


def obj_to_dict(obj: Any, base_dict={}) -> dict:
    """
    Creates nested dictionaries from input object
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
            elif type(value) in [list, tuple]:
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

            elif isinstance(value, Enum):
                value = value.name

            # Value has been created so set the dictionary item
            output[attr_name] = value
    return output


def dict_to_obj(input: dict, base_object_class, references: dict = {}) -> object:
    obj, refs = dict_to_obj_pass1(input, base_object_class)
    dict_to_obj_pass2(obj, refs)
    return obj


def dict_to_obj_pass2(obj: Any, references: dict) -> None:
    """
    Pass 2 walks through objects and replaces attributes which are references with the actual class.
    """
    type_dict: dict = get_type_hints(type(obj))

    # Loop through all type hints on object
    for attr_name in type_dict.keys():
        # Walk through all attributes of object
        if hasattr(obj, attr_name):
            value = getattr(obj, attr_name)
            obj_attr_type = type_dict[attr_name]

            if type(value) == list:
                # We have a list if its supposed to be a list of classes then examine
                if obj_attr_type.__args__[0] not in DEFAULT_TYPES:
                    new_list = []
                    for item in value:
                        # If item is supposed to be a class but is actually a default type then must be reference
                        if type(item) in DEFAULT_TYPES:
                            new_list.append(references[value])
                        else:
                            dict_to_obj_pass2(item, references)
                            new_list.append(item)
                    setattr(obj, attr_name, new_list)

            elif obj_attr_type not in DEFAULT_TYPES:
                # If value is supposed to be a class but is actually a default type then must be reference
                if type(value) in DEFAULT_TYPES:
                    setattr(obj, attr_name, references[value])
                # If value is a class then parse it
                else:
                    dict_to_obj_pass2(value, references)


def dict_to_obj_pass1(input: dict, base_object_class, references: dict = {}) -> Tuple[Any, dict]:
    """
    Creates objects from input dictionary. Pass 1 keeps references and compiles a list of objects with ids used in pass 2.
    """
    # Instantiate the requested class & get the type hints
    obj = base_object_class()
    type_dict = get_type_hints(type(obj))

    for attr_name in type_dict.keys():
        if attr_name in input.keys():
            # The input has this item defined in the class so extract
            # dict_attr_type = type(input[attr_name])  # type_dict[attr_name].__origin__ TODO: use definition rather than input
            obj_attr_type = type_dict[attr_name]

            if type(input[attr_name]) != list:
                if obj_attr_type in DEFAULT_TYPES:
                    # Value definition is standard type so just set the value
                    setattr(obj, attr_name, input[attr_name])
                elif type(input[attr_name]) == dict:
                    # Not a standard type, represented as dict. Recurse to expand sub-object
                    new_obj, new_refs = dict_to_obj_pass1(input[attr_name], type_dict[attr_name], references)
                    setattr(obj, attr_name, new_obj)
                    # Store object in reference dictionary and add new object
                    references.update(new_refs)
                    references[getattr(new_obj, new_obj.Meta.id_field)] = new_obj
                else:
                    # If definition is class and dict value has string then must be a reference using id_field value from Meta
                    setattr(obj, attr_name, input[attr_name])
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
                            new_obj, new_refs = dict_to_obj_pass1(item, item_type)
                            value.append(new_obj)
                            # Store object in reference dictionary and add new object
                            references.update(new_refs)
                            references[getattr(new_obj, new_obj.Meta.id_field)] = new_obj
                        else:
                            # If definition is class and dict value has string then must be a reference using id_field value from Meta
                            value.append(item)
                setattr(obj, attr_name, value)
    return obj, references
