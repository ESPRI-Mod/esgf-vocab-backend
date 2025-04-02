import json
from typing import Iterable, Mapping

from esgvoc.apps.drs.report import DrsGenerationReport
from fastapi import FastAPI
from fastapi.testclient import TestClient

import esgvoc_backend.drs as drs
from tests.api_inputs import (  # noqa: F401
    DrsMappingGeneratorExpression,
    DrsTermsGeneratorExpression,
    check_drs_generated_expression,
    drs_generation_expression,
)
from tests.utils import convert_drs_type

_BASE_URL = 'http://localhost:9999/apps/drs'


_APP = FastAPI()
_APP.include_router(drs.router)
_CLIENT = TestClient(_APP, base_url=_BASE_URL, backend='asyncio')


def _check_generation(drs_generation_expression: DrsTermsGeneratorExpression |
                                                 DrsMappingGeneratorExpression) -> None:
    body: Iterable | Mapping
    if isinstance(drs_generation_expression, DrsMappingGeneratorExpression):
        url_discriminant = 'mapping'
        body = drs_generation_expression.mapping
    else:
        url_discriminant = 'terms'
        body = drs_generation_expression.terms
    drs_type = convert_drs_type(drs_generation_expression.drs_type)
    url = f"/{drs_generation_expression.project_id}/generation/{url_discriminant}/{drs_type}"
    result = _CLIENT.post(url=url, data=json.dumps(body))  # type: ignore
    result.raise_for_status()
    report = DrsGenerationReport(**result.json())
    check_drs_generated_expression(drs_generation_expression, report)


def test_terms_generation(drs_generation_expression) -> None:
    _check_generation(drs_generation_expression)
