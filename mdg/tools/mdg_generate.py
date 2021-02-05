#!/usr/bin/python
# This file is used as an entry point so requires mdg package to be installed into site-packages
# So after a pip or setup.py install you can just cd to the recipie folder and call mdg_generate

import sys
import os


def main():
    if len(sys.argv) == 1:
        recipie_path = './config.yaml'
    else:
        recipie_path = str(sys.argv[1])

    os.environ.setdefault("PYMDG_SETTINGS_MODULE", recipie_path)

    from ..generate import generate
    generate()


if __name__ == '__main__':
    main()
