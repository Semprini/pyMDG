#!/usr/bin/python
from .validate import validate_package
from .render import output_model, output_test_cases
from .parse import parse, ParseError


def generate():
    """ Loads XMI file from settings as an etree
        Calls XMI parser to turn model and tests into python native (see UML metamodel)
        Calls output functions to render for model and tests
    """

    try:
        model_package, test_cases = parse()

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
    except ParseError as e:
        print(e)
