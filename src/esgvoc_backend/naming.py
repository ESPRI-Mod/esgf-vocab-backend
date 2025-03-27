API_WEB_DOCUMENTATION_URL_PREFIX = 'https://esgf.github.io/esgf-vocab/api_documentation'
API_VERSION = 'v1'
API_PREFIX = f'/api/{API_VERSION}'

# Prefix for the API Web documentation of the route.
UNIVERSE_PAGE_PREFIX = 'universe.html#esgvoc.api.universe'
PROJECTS_PAGE_PREFIX = 'projects.html#esgvoc.api.projects'
DRS_GEN_PREFIX = 'drs.html#esgvoc.apps.drs.generator.DrsGenerator'
DRS_VAL_PREFIX = 'drs.html#esgvoc.apps.drs.validator.DrsValidator'


def generate_route_desc(*url_postfixes: str) -> str:
    result = 'API documentation '
    for url_postfix in url_postfixes:
        result += f'[{url_postfix.split('.')[-1]}]({API_WEB_DOCUMENTATION_URL_PREFIX}/{url_postfix}), '
    return result[: -2] + '.'
