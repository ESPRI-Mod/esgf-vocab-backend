API_WEB_DOCUMENTATION_URL_PREFIX = 'https://esgf.github.io/esgf-vocab/api_documentation'


def _generate_route_desc(url_postfix: str) -> str:
    return f'API documentation [link]({API_WEB_DOCUMENTATION_URL_PREFIX}/{url_postfix}).'
