from typing import Any, Generator

import pytest
from esgvoc.apps.drs.report import DrsValidationReport
from fastapi import FastAPI
from fastapi.testclient import TestClient

import esgvoc_backend.drs as drs

_BASE_URL = 'http://localhost:9999/drs'


_APP = FastAPI()
_APP.include_router(drs.router)
_CLIENT = TestClient(_APP, base_url=_BASE_URL, backend='asyncio')


_SOME_VALIDATION_PARAMS = [
    {'project_id': 'cmip6plus',
     'drs_type': 'directory',
     'expression_ok': 'CMIP6Plus/CMIP/NCC/MIROC6/amip/r2i2p1f2/ACmon/od550aer/gn/v20190923',
     'expression_ko': 'CMIP6Plus/CMIP/NCC/MIROC6/amip/ /r2i2p1f2/ACmon/od550aer/gn',
     'error_kinds': ['BlankTerm', 'MissingTerm']},

    {'project_id': 'cmip6plus',
     'drs_type': 'datasetid',
     'expression_ok': 'CMIP6Plus.CMIP.IPSL.MIROC6.amip.r2i2p1f2.ACmon.od550aer.gn',
     'expression_ko': 'CMIP6Plus.CMIP.IPSL.MIROC6.amip.r2i2p1f2.ACmon.od550aer.gn.',
     'error_kinds': ['ExtraChar']},

    {'project_id': 'cmip6plus',
     'drs_type': 'filename',
     'expression_ok': 'od550aer_ACmon_MIROC6_amip_r2i2p1f2_gn_201211-201212.nc',
     'expression_ko': 'od550aer_ACmon_MIROC6_amip_r2i2p1f2_GUXX.nc',
     'error_kinds': ['InvalidTerm']},
]


def _provide_validation_params() -> Generator:
    for expression in _SOME_VALIDATION_PARAMS:
        yield expression


@pytest.fixture(params=_provide_validation_params())
def validation_param(request) -> dict[str, Any]:
    return request.param


def test_validation(validation_param) -> None:
    url = f"/{validation_param['project_id']}/validation/{validation_param['drs_type']}"
    result = _CLIENT.get(url=url, params={'expression': validation_param['expression_ok']})
    result.raise_for_status()
    report = DrsValidationReport(**result.json())
    assert report.validated
    result = _CLIENT.get(url=url, params={'expression': validation_param['expression_ko']})
    result.raise_for_status()
    report = DrsValidationReport(**result.json())
    assert report.nb_errors == len(validation_param['error_kinds'])
    for index in range(0, len(report.errors)):
        assert report.errors[index].kind == validation_param['error_kinds'][index]
