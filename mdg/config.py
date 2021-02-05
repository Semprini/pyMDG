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
    config_filename = os.environ.get('PYMDG_SETTINGS_MODULE', "")
    try:
        with open(config_filename, 'r') as config_file:
            loaded_settings = yaml.load(config_file.read(), Loader=yaml.SafeLoader)
        settings = {**defaults, **loaded_settings}
        print("Config file loaded: " + config_filename)
        return settings
    except TypeError as e:
        print("WARN: Config file {} could not be parsed. Using default settings. Reason: {}".format(config_filename, e.message))
    except FileNotFoundError:
        print("WARN: Config file {} not found. Using default settings".format(config_filename))
    return defaults


settings = load()
