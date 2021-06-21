#!/usr/bin/python
# This file is used as an entry point so requires mdg package to be installed into site-packages
# So after a pip or setup.py install you can just cd to the recipe folder and call mdg_generate

# import sys
import os
import logging


logger = logging.getLogger('mdg')
logger.propagate = False
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def generate(args):
    os.environ.setdefault("PYMDG_SETTINGS_MODULE", args.recipe_path)
    from ..generate import generate
    generate()


def validate(args):
    os.environ.setdefault("PYMDG_SETTINGS_MODULE", args.recipe_path)
    from ..validate import validate
    validate()


def dumps(args):
    os.environ.setdefault("PYMDG_SETTINGS_MODULE", args.recipe_path)
    from ..uml import dumps
    from ..parse import parse

    model_package, test_cases = parse()
    print(dumps(model_package))


def startproject(args):
    print('Not Implemented Yet')
    print('Val:((%s))' % args)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Model Driven Generation Engine')
    subparsers = parser.add_subparsers(title='subcommands', description='valid subcommands', help='subcommand help')

    parser_a = subparsers.add_parser('generate', help='Generate files from a model using a recipe')
    parser_a.add_argument('recipe_path', type=str, help='The path to the recipe config file')
    parser_a.set_defaults(func=generate)

    parser_b = subparsers.add_parser('validate', help='Validate files for a model using a recipe')
    parser_b.add_argument('recipe_path', type=str, help='The path to the recipe config file')
    parser_b.set_defaults(func=validate)

    parser_a = subparsers.add_parser('dumps', help='Outputs parsed model as JSON')
    parser_a.add_argument('recipe_path', type=str, help='The path to the recipe config file')
    parser_a.set_defaults(func=dumps)

    parser_c = subparsers.add_parser('startproject', help='Create project with recipe and templates')
    parser_c.add_argument('project_type', choices=['django', 'schema', 'java'], help='The type of project')
    parser_c.add_argument('project_path', type=str, help='The path to the project')
    parser_c.set_defaults(func=startproject)

    args = parser.parse_args()
    try:
        func = args.func
    except AttributeError:  # (https://bugs.python.org/issue16308)
        parser.error("too few arguments")
    func(args)


if __name__ == '__main__':
    main()
