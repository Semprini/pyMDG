from ..config import settings
from .case import camelcase, snakecase, titlecase, sentencecase, uppercase


def get_filters():
    # Create jinja2 filter dict to pass into templates
    filters = {
        'camelcase': camelcase,
        'snakecase': snakecase,
        'titlecase': titlecase,
        'sentencecase': sentencecase,
        'uppercase': uppercase,
    }

    if settings['case_package'] == "CamelCase":
        filters['case_package'] = camelcase
    elif settings['case_package'] == "snake_case":
        filters['case_package'] = snakecase
    else:
        filters['case_package'] = camelcase

    if settings['case_class'] == "CamelCase":
        filters['case_class'] = camelcase
    elif settings['case_class'] == "snake_case":
        filters['case_class'] = snakecase
    else:
        filters['case_class'] = camelcase

    if settings['case_attribute'] == "CamelCase":
        filters['case_attribute'] = camelcase
    elif settings['case_attribute'] == "snake_case":
        filters['case_attribute'] = snakecase
    else:
        filters['case_class'] = snakecase

    return filters
