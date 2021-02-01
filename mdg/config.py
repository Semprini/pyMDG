import os
import yaml
from typing import Dict, List

model_templates: List[Dict] = []

defaults: Dict = {
    "generation_type": "default",
    "root_package": "default",
    "model_templates": model_templates,
    "case_package": "CamelCase",
    "case_class": "CamelCase",
    "case_attribute": "snake_case",
    "parser": None,
}


def load():
    try:
        with open(os.environ.get('PYMDG_SETTINGS_MODULE', ""), 'r') as config_file:
            loaded_settings = yaml.load(config_file.read(), Loader=yaml.SafeLoader)
        settings = {**defaults, **loaded_settings}
        print("Config file loaded: " + os.environ.get('PYMDG_SETTINGS_MODULE', ""))
        return settings
    except TypeError:
        print("WARN: Config file could not be parsed. Using default settings")
    except FileNotFoundError:
        print("WARN: Config file not found. Using default settings")
    return defaults


settings = load()
