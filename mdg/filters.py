from .config import settings
from .util import camelcase, snakecase, titlecase, sentencecase


def get_filters():
    # Create jinja2 filter dict to pass into templates
    filters = {
        'camelcase': camelcase,
        'snakecase': snakecase,
        'titlecase': titlecase,
        'sentencecase': sentencecase,
    }
    if settings['case_package'] == "CamelCase":
        filters['case_package'] = camelcase
    elif settings['case_package'] == "snake_case":
        filters['case_package'] = snakecase
    if settings['case_class'] == "CamelCase":
        filters['case_class'] = camelcase
    elif settings['case_class'] == "snake_case":
        filters['case_class'] = snakecase
    if settings['case_attribute'] == "CamelCase":
        filters['case_attribute'] = camelcase
    elif settings['case_attribute'] == "snake_case":
        filters['case_attribute'] = snakecase

    return filters
