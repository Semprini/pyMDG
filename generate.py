#!/usr/bin/python
import sys
import os


def main():
    if len(sys.argv) == 1:
        recipie_path = './sample_recipie'
    else:
        recipie_path = str(sys.argv[1])

    config_filename = recipie_path + "/config.yaml"
    os.environ.setdefault("PYMDG_SETTINGS_MODULE", config_filename)

    from mdg.xmi import generator
    generator.parse()


if __name__ == '__main__':
    main()
