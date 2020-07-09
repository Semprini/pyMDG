#!/usr/bin/python
# This file is used as an entry point so requires mdg package to be installed into site-packages
# So after a pip or setup.py install you can just cd to the recipie folder and call mdg_generate
import sys
import os


def main():
    if len(sys.argv) == 1:
        recipie_path = '.'
    else:
        recipie_path = str(sys.argv[1])

    config_filename = recipie_path + "/config.yaml"
    os.environ.setdefault("PYMDG_SETTINGS_MODULE", config_filename)

    from mdg import generator
    generator.xmi_parse()


if __name__ == '__main__':
    main()
