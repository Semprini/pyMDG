#!/usr/bin/python
import logging

from mdg.uml.validate import validate_package
from mdg.generate.render import output_model, output_test_cases
from mdg.parse import parse, ParseError, PARSERS
from mdg.config import settings
from mdg import generation_fields

logger = logging.getLogger('mdg')


def validate_settings():
    logger.debug("Validating settings")
    
    errors = []
    if settings['default_dialect'] not in generation_fields.keys():
        errors.append( f"Settings default_dialect of '{settings['default_dialect']}' is not valid. Generation types are a dictionay of how to map UML attrribute types to physical types. Options are: {generation_fields.keys()}" )

    if settings['parser'] not in PARSERS.keys():
        errors.append( f"Settings parser of '{settings['parser']}' is not valid. Parser must match the input modelling tool type defined in 'source'. Options are: {PARSERS.keys()}" )

    for template_definition in settings['generation_artifacts']:
        levels = ["root","copy","class","package","enumeration","assocication"]
        if template_definition["level"] not in levels:
            errors.append( f"Template level of '{template_definition['level']}' is not valid. Level defines how many times the output will be rendered and the objects passed to the template. Options are: {levels}" )

    if errors != []:
        logger.error(f"Errors in settings: {errors}")
        return False
    
    return True


def generate():
    """ Loads XMI file from settings as an etree
        Calls XMI parser to turn model and tests into python native (see UML metamodel)
        Calls output functions to render for model and tests
    """
    if not validate_settings():
        logger.error("Due to errors in settings, not parsing or generating.")
        return

    logger.debug("generate begin")
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
        if 'test_package' in settings.keys():
            output_test_cases(test_cases)

    except ParseError as e:
        logger.error(e)
    logger.debug("generate end")
