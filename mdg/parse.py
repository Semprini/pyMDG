#!/usr/bin/python
import logging

from .config import settings
from .sparx_xmi.parse import parse_uml as sparx_parse_uml
from .drawio_xml.parse import parse_uml as drawio_parse_uml


logger = logging.getLogger(__name__)


class ParseError(Exception):
    pass


def parse():
    """ Loads XMI file from settings as an etree
        Calls XMI parser to turn model and tests into python native (see UML metamodel)
    """
    logger.debug("parse begin")

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
    logger.info("Base Model Package: " + model_package.name)

    logger.debug("parse end")
    return model_package, test_cases
