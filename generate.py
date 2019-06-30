#!/usr/bin/python
import sys
from xmi import generator

if __name__ == '__main__':
    if len(sys.argv) == 1:
        recipie_path = 'test_recipie'
    else:
        recipie_path = str(sys.argv[1])

    generator.parse(recipie_path)
    