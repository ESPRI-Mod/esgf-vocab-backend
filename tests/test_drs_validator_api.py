from esgvoc.apps.drs.report import DrsValidationReport
from fastapi import FastAPI
from fastapi.testclient import TestClient

import esgvoc_backend.drs as drs
from tests.api_inputs import check_drs_validation_expression, drs_validation_query  # noqa: F401
from tests.utils import convert_drs_type

_BASE_URL = 'http://localhost:9999/apps/drs'


_APP = FastAPI()
_APP.include_router(drs.router)
_CLIENT = TestClient(_APP, base_url=_BASE_URL, backend='asyncio')


def test_validation(drs_validation_query) -> None:
    drs_type = convert_drs_type(drs_validation_query.drs_type)
    url = f"/{drs_validation_query.project_id}/validation/{drs_type}"
    result = _CLIENT.get(url=url, params={'expression': drs_validation_query.expression})
    result.raise_for_status()
    report = DrsValidationReport(**result.json())
    check_drs_validation_expression(drs_validation_query, report)
