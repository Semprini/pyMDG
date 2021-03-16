import os
import yaml
from typing import Dict, List
import logging


logger = logging.getLogger(__name__)

model_templates: List[Dict] = []

defaults: Dict = {
    "generation_type": "default",
    "root_package": "default",
    "model_templates": model_templates,
    "case_package": "CamelCase",
    "case_class": "CamelCase",
    "case_attribute": "snake_case",
    "parser": None,
    "use_alias": True,
}


def load():
    config_filename = os.environ.get('PYMDG_SETTINGS_MODULE', "")
    try:
        with open(config_filename, 'r') as config_file:
            loaded_settings = yaml.load(config_file.read(), Loader=yaml.SafeLoader)
        settings = {**defaults, **loaded_settings}
        logger.info("Config file loaded: " + config_filename)
        return settings
    except TypeError as e:
        logger.warning("Config file {} could not be parsed. Using default settings. Reason: {}".format(config_filename, e.message))
    except FileNotFoundError:
        logger.warning("WARN: Config file {} not found. Using default settings".format(config_filename))
    return defaults


settings = load()
