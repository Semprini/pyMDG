import os
import yaml

settings = {
    "generation_type": "default",
}

try:
    with open(os.environ.get('PYMDG_SETTINGS_MODULE', ""), 'r') as config_file:
        settings = yaml.load(config_file.read(), Loader=yaml.SafeLoader)
except FileNotFoundError:
    print("Using default settings")
