#!/usr/bin/python
import sys
import os
import logging


logger = logging.getLogger('mdg')
logger.propagate = False
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


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
