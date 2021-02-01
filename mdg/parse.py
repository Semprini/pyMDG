#!/usr/bin/python
from .config import settings
from .sparx_xmi.parse import parse_uml as sparx_parse_uml
from .drawio_xml.parse import parse_uml as drawio_parse_uml


class ParseError(Exception):
    pass


def parse():
    """ Loads XMI file from settings as an etree
        Calls XMI parser to turn model and tests into python native (see UML metamodel)
    """

    # TODO: change to using a registration decorator
    PARSERS = {
        'sparx': sparx_parse_uml,
        'drawio': drawio_parse_uml,
    }

    # Find the parser
    parser = None
    try:
        parser = PARSERS[settings['parser']]
    except KeyError:
        raise ParseError("Error: Could not find parser. Settings must specify sparx or drawio")

    # Call the parser
    model_package, test_cases = parser()
    model_package.name = settings['root_package']
    print("Base Model Package: " + model_package.name)

    return model_package, test_cases
