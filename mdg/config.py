import os
import yaml
from typing import Dict, List

model_templates: List[Dict] = []

settings: Dict = {
    "generation_type": "default",
    "root_package": "default",
    "model_templates": model_templates,
    "case_package": "CamelCase",
    "case_class": "CamelCase",
    "case_attribute": "snake_case",
}

try:
    with open(os.environ.get('PYMDG_SETTINGS_MODULE', ""), 'r') as config_file:
        loaded_settings = yaml.load(config_file.read(), Loader=yaml.SafeLoader)
    settings = {**settings, **loaded_settings}
    print("Config file loaded: " + os.environ.get('PYMDG_SETTINGS_MODULE', ""))
except FileNotFoundError:
    print("WARN: Config file not found. Using default settings")
