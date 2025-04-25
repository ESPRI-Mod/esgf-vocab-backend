from typing import Any

from fastapi import HTTPException, status

from esgvoc_backend.naming import API_WEB_DOCUMENTATION_URL_PREFIX


def check_result(result: Any | None) -> Any:
    if result:
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def generate_route_desc(*url_postfixes: str) -> str:
    result = 'API documentation '
    for url_postfix in url_postfixes:
        result += f'[{url_postfix.split('.')[-1]}]({API_WEB_DOCUMENTATION_URL_PREFIX}/{url_postfix}), '
    return result[: -2] + '.'
