#!/usr/bin/python
# This file is used as an entry point so requires mdg package to be installed into site-packages
# So after a pip or setup.py install you can just cd to the recipie folder and call mdg_generate
import sys
import os


def generate():
    """ Loads XMI file from settings as an etree
        Calls XMI parser to turn model and tests into python native (see UML metamodel)
        Calls output functions to render for model and tests
    """
    from .config import settings
    from .validate import validate_package
    from .render import output_model, output_test_cases
    from .sparx_xmi.parse import parse_uml as sparx_parse_uml
    from .drawio_xml.parse import parse_uml as drawio_parse_uml

    # TODO: change to using a registration decorator
    PARSERS = {
        'sparx': sparx_parse_uml,
        'drawio': drawio_parse_uml,
    }

    # Call the parser
    model_package, test_cases = PARSERS[settings['parser']]()
    print("Base Model Package: " + model_package.name)

    # Validate the parsed model package
    errors = validate_package(model_package)
    if len(errors) > 0:
        print("Validation Errors:")
        for error in errors:
            print("    {}".format(error))

    # TODO: Validate the test cases

    # Generate files from the native python UML
    output_model(model_package)
    output_test_cases(test_cases)


def main():
    if len(sys.argv) == 1:
        recipie_path = './config.yaml'
    else:
        recipie_path = str(sys.argv[1])

    config_filename = recipie_path
    os.environ.setdefault("PYMDG_SETTINGS_MODULE", config_filename)

    generate()


if __name__ == '__main__':
    main()
