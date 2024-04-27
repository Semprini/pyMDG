import os
import yaml
from typing import Dict, List
import logging


logger = logging.getLogger(__name__)

generation_artifacts: List[Dict] = []

defaults: Dict = {
    "default_dialect": "default",
    "root_package": "default",
    "generation_artifacts": generation_artifacts,
    "case_package": "PascalCase",
    "case_class": "PascalCase",
    "case_attribute": "snake_case",
    "parser": None,
    "use_alias": True,
    "default_string_length": 50,
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


# If no recipe has been set before now, assume test recipe
if os.environ.get('PYMDG_SETTINGS_MODULE', None) is None:
    recipe_path = './sample_recipes' + "/config-test.yaml"
    os.environ.setdefault("PYMDG_SETTINGS_MODULE", recipe_path)

settings = load()
