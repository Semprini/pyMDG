#!/usr/bin/python
# This file is used as an entry point so requires mdg package to be installed into site-packages
# So after a pip or setup.py install you can just cd to the recipe folder and call mdg_generate

# import sys
import os
import logging


logger = logging.getLogger('mdg')
logger.propagate = False
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
    from ..uml.validate import validate
    validate()


def dumps(args):
    os.environ.setdefault("PYMDG_SETTINGS_MODULE", args.recipe_path)
    from ..uml import dumps as uml_dumps
    from ..parse import parse

    model_package, test_cases = parse()
    print(uml_dumps(model_package))


def startproject(args):
    """ mdg-tool startproject --source="sqlite:///Customer Model.qea" --parser=sparx --model_package=<GUID> --default_dialect=django config-customer-graphql.yaml
    """
    
    with open(args.project_path, "w") as f:
        f.write(f"source: {args.source}\n")
        f.write(f"parser: {args.parser}\n")
        f.write(f'model_package: "{args.model_package}"\n')
        f.write("dest_root: ./build\n")
        f.write(f"templates_folder: ./templates\n")
        f.write(f"default_dialect: {args.default_dialect}\n")
        f.write("generation_artifacts:\n")


def addtemplate(args):
    """
    """
    templates = {
        "django_model":"""
- dest: "{{package.root_package.name | camelcase}}/{{package.name | camelcase}}/models.py"
  level: package
  source: "django/app/models.py.jinja"
  filter: "{% if package.classes != [] %}True{% else %}False{% endif %}"
""",
        "hasura":"""
- dest: "{{package.root_package.name | camelcase}}/hasura_metadata.json"
  level: root
  source: "hasura.json.jinja"  
"""}
    with open(args.project_path, "a") as f:
        f.write(templates[args.template_type])


def daemon(args):
    os.environ.setdefault("PYMDG_SETTINGS_MODULE", args.recipe_path)
    from mdg.tools.daemon import poller
    poller(args.poll_seconds)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Model Driven Generation Engine')
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
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
    parser_c.add_argument('-s', '--source', type=str, help="The source model file/DB connection")
    parser_c.add_argument('-p', '--parser', type=str, choices=['sparx', 'sparxdb', 'drawio'], help='The format of the source.')
    parser_c.add_argument('-d', '--default_dialect', type=str, choices=['default', 'django', 'schema', 'java'], help='The dialect to use if not specified per artifact')
    parser_c.add_argument('-m', '--model_package', type=str, help='The ID of the root package in ther source.')
    parser_c.add_argument('project_path', type=str, help='The path to the project')
    parser_c.set_defaults(func=startproject)

    parser_c = subparsers.add_parser('addtemplate', help='Add a generation template to a config')
    parser_c.add_argument('template_type', type=str, choices=["django_model", "hasura"], help='The type of template to add')
    parser_c.add_argument('project_path', type=str, help='The path to the project')
    parser_c.set_defaults(func=addtemplate)

    parser_d = subparsers.add_parser('daemon', help='Poll package versions and run generation jobs on change')
    parser_d.add_argument('recipe_path', type=str, help='The path to the recipe config file')
    parser_d.add_argument('poll_seconds', type=int, help='Seconds between polls')
    parser_d.set_defaults(func=daemon)

    args = parser.parse_args()
    if args.verbose == 0:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)
    try:
        func = args.func
    except AttributeError:  # (https://bugs.python.org/issue16308)
        parser.error("too few arguments")
    func(args)


if __name__ == '__main__':
    main()
