#!/usr/bin/python
import sys
import os


def main():
    if len(sys.argv) == 1:
        recipie_path = './config.yaml'
    else:
        recipie_path = str(sys.argv[1])

    os.environ.setdefault("PYMDG_SETTINGS_MODULE", recipie_path)

    from ..validate import validate
    validate()


if __name__ == '__main__':
    main()
