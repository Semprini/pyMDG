#!/usr/bin/python
import sys
import os


if __name__ == '__main__':
    if len(sys.argv) == 1:
        recipie_path = './sample_recipie' + "/config.yaml"
    else:
        recipie_path = str(sys.argv[1])

    config_filename = recipie_path
    os.environ.setdefault("PYMDG_SETTINGS_MODULE", config_filename)

    from mdg.generate import main
    main()
