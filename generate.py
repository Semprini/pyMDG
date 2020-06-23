#!/usr/bin/python
import sys, os



if __name__ == '__main__':
    if len(sys.argv) == 1:
        recipie_path = 'sample_recipie'
    else:
        recipie_path = str(sys.argv[1])

    config_filename = recipie_path + "/config.yaml"
    os.environ.setdefault("PYXMI_SETTINGS_MODULE", config_filename)

    from mdg.xmi import generator
    generator.parse(recipie_path)
    