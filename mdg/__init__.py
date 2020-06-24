import os
import yaml

settings = {
    "generation_type": "default",
}

generation_fields = {
    "default": {
        "boolean": "boolean",
        "date": "Date",
        "dateTime": "DateTime",
        "decimal": "Double",
        "enum": "String",
        "int": "int",
        "bigint": "int",
        "integer": "int",
        "long": "int",
        "string": "String",
    },
    "spring data rest": {
        "boolean": "boolean",
        "date": "Date",
        "dateTime": "DateTime",
        "decimal": "Double",
        "enum": "String",
        "int": "int",
        "bigint": "int",
        "integer": "int",
        "long": "int",
        "string": "String",
    },
    "django": {
        "boolean": "BooleanField",
        "int": "IntegerField",
        "bigint": "BigIntegerField",
        "decimal": "DecimalField",
        "string": "CharField",
        "text": "TextField",
        "duration": "DurationField",
        "file": "FileField",
        "float": "FloatField",
    },
    "marshmallow": {
        "boolean": "Boolean",
        "int": "Integer",
        "integer": "Integer",
        "bigint": "Integer",
        "decimal": "Decimal",
        "string": "String",
        "text": "Text",
        "duration": "Duration",
        "file": "File",
        "float": "Float",
        "date": "Date",
        "dateTime": "DateTime",
        "date_time": "DateTime",
    }
}

try:
    with open(os.environ.get('PYXMI_SETTINGS_MODULE', ""), 'r') as config_file:
        settings = yaml.load(config_file.read(), Loader=yaml.SafeLoader)
except FileNotFoundError:
    print("Using default settings")
