import pytest
from esgvoc.apps.drs.report import DrsValidationReport
from fastapi import FastAPI

import esgvoc_backend.drs as drs
from tests.api_inputs import check_drs_validation_expression, drs_validation_query  # noqa: F401
from tests.utils import client_factory, convert_drs_type

router = drs.router
_APP = FastAPI()
_APP.include_router(router)

@pytest.fixture(scope='module')
def client(request):
    return client_factory(request, router)


def test_validation(client, drs_validation_query) -> None:
    drs_type = convert_drs_type(drs_validation_query.drs_type)
    url = f"/{drs_validation_query.project_id}/validation/{drs_type}"
    result = client.get(url=url, params={'expression': drs_validation_query.expression})
    result.raise_for_status()
    report = DrsValidationReport(**result.json())
    check_drs_validation_expression(drs_validation_query, report)
