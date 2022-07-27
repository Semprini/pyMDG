#!/usr/bin/python
import logging

from mdg.config import settings
from .sparx_xmi import parse_uml as sparx_parse_uml
from .drawio_xml import parse_uml as drawio_parse_uml
from .bouml_xmi import parse_uml as bouml_parse_uml
from .sparx_db import parse_uml as sparx_db_parse_uml


logger = logging.getLogger(__name__)


class ParseError(Exception):
    pass


def parse():
    """ Calls parser to turn model and tests into python native (see UML metamodel)
    """
    logger.debug("parse begin")

    # TODO: change to using a registration decorator
    PARSERS = {
        'sparx': sparx_parse_uml,
        'sparxdb': sparx_db_parse_uml,
        'drawio': drawio_parse_uml,
        'bouml': bouml_parse_uml,
    }

    # Find the parser
    parser = None
    try:
        parser = PARSERS[settings['parser']]
        logger.debug(f"{settings['parser']} parser selected")
    except KeyError:
        raise ParseError("Error: Could not find parser. Settings must specify sparx, bouml or drawio")

    # Call the parser
    model_package, test_cases = parser()
    model_package.name = settings['root_package']
    logger.info("Base Model Package: " + model_package.name)

    logger.debug("parse end")
    return model_package, test_cases
