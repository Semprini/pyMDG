#!/usr/bin/python
import sys
import os

from ..validate import validate


def main():
    if len(sys.argv) == 1:
        recipie_path = './config.yaml'
    else:
        recipie_path = str(sys.argv[1])

    config_filename = recipie_path
    os.environ.setdefault("PYMDG_SETTINGS_MODULE", config_filename)

    validate()


if __name__ == '__main__':
    main()
