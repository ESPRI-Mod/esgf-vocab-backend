import json
from typing import Any, Generator

import pytest
from esgvoc.apps.drs.report import DrsGenerationReport
from fastapi import FastAPI
from fastapi.testclient import TestClient

import esgvoc_backend.drs as drs

_BASE_URL = 'http://localhost:9999/drs'


_APP = FastAPI()
_APP.include_router(drs.router)
_CLIENT = TestClient(_APP, base_url=_BASE_URL, backend='asyncio')


_SOME_MAPPING_GENERATION_PARAMS = [
    {'project_id': 'cmip6plus',
     'drs_type': 'directory',
     'mapping_ok': {
        'member_id': 'r2i2p1f2',
        'activity_id': 'CMIP',
        'source_id': 'MIROC6',
        'mip_era': 'CMIP6Plus',
        'experiment_id': 'amip',
        'variable_id': 'od550aer',
        'table_id': 'ACmon',
        'grid_label': 'gn',
        'version': 'v20190923',
        'institution_id': 'IPSL'},
     'gen_expr_ok': 'CMIP6Plus/CMIP/IPSL/MIROC6/amip/r2i2p1f2/ACmon/od550aer/gn/v20190923',
     'mapping_ko': {
        'member_id': 'r2i2p1f2',
        'activity_id': 'CMIP',
        'source_id': 'MIROC6',
        'mip_era': 'CMIP6Plus',
        'experiment_id': 'ERROR',
        'variable_id': 'od550aer',
        'table_id': 'ACmon',
        'grid_label': 'gn',
        'institution_id': 'IPSL'},
     'gen_expr_ko': 'CMIP6Plus/CMIP/IPSL/MIROC6/[INVALID]/r2i2p1f2/ACmon/od550aer/gn/[MISSING]',
     'error_kinds': ['InvalidTerm', 'MissingTerm']},

    {'project_id': 'cmip6plus',
     'drs_type': 'filename',
     'mapping_ok': {
        'member_id': 'r2i2p1f2',
        'activity_id': 'CMIP',
        'source_id': 'MIROC6',
        'mip_era': 'CMIP6Plus',
        'experiment_id': 'amip',
        'variable_id': 'od550aer',
        'table_id': 'ACmon',
        'grid_label': 'gn',
        'institution_id': 'IPSL'},
     'gen_expr_ok': 'od550aer_ACmon_MIROC6_amip_r2i2p1f2_gn.nc',
     'mapping_ko': {
        'member_id': 'r2i2p1f2',
        'activity_id': 'CMIP',
        'source_id': 'MIROC6',
        'mip_era': 'CMIP6Plus',
        'xperiment_id': 'amip',
        'variable_id': 'od550aer',
        'table_id': 'ACmon',
        'grid_label': 'gn',
        'institution_id': 'IPSL'},
     'gen_expr_ko': 'od550aer_ACmon_MIROC6_[MISSING]_r2i2p1f2_gn.nc',
     'error_kinds': ['MissingTerm']},

    {'project_id': 'cmip6plus',
     'drs_type': 'datasetid',
     'mapping_ok': {
        'member_id': 'r2i2p1f2',
        'activity_id': 'CMIP',
        'source_id': 'MIROC6',
        'mip_era': 'CMIP6Plus',
        'experiment_id': 'amip',
        'variable_id': 'od550aer',
        'table_id': 'ACmon',
        'grid_label': 'gn',
        'institution_id': 'IPSL'},
     'gen_expr_ok': 'CMIP6Plus.CMIP.IPSL.MIROC6.amip.r2i2p1f2.ACmon.od550aer.gn',
     'mapping_ko': {
        'member_id': 'r2i2p1f2',
        'activity_id': 'CMIP',
        'source_id': 'MIROC6',
        'mip_era': 'CMIP6Plus',
        'experiment_id': 'amip',
        'variable_id': 'od550aer',
        'table_id': 'ACmon',
        'grid_label': 'Grrrr',
        'institution_id': 'IPSL'},
     'gen_expr_ko': 'CMIP6Plus.CMIP.IPSL.MIROC6.amip.r2i2p1f2.ACmon.od550aer.[INVALID]',
     'error_kinds': ['InvalidTerm']},
]

_SOME_TERMS_GENERATION_PARAMS = [
    {'project_id': 'cmip6plus',
     'drs_type': 'directory',
     'terms_ok': ['r2i2p1f2', 'CMIP', 'MIROC6', 'CMIP6Plus', 'amip', 'od550aer', 'ACmon', 'gn',
                  'v20190923', 'IPSL'],
     'gen_expr_ok': 'CMIP6Plus/CMIP/IPSL/MIROC6/amip/r2i2p1f2/ACmon/od550aer/gn/v20190923',
     'terms_ko': ['r2i2p1f2', 'CMIP', 'MIROC6', 'CMIP6Plus', 'DKRZ', 'od550aer', 'ACmon', 'gn', 'IPSL'],
     'gen_expr_ko': 'CMIP6Plus/CMIP/[MISSING]/MIROC6/[MISSING]/r2i2p1f2/ACmon/od550aer/gn/[MISSING]',
     'error_kinds': ['TooManyTermsCollection', 'MissingTerm', 'MissingTerm', 'MissingTerm']},

    {'project_id': 'cmip6plus',
     'drs_type': 'filename',
     'terms_ok': ['r2i2p1f2', 'CMIP', 'MIROC6', 'CMIP6Plus', 'amip', 'od550aer', 'ACmon', 'gn'],
     'gen_expr_ok': 'od550aer_ACmon_MIROC6_amip_r2i2p1f2_gn.nc',
     'terms_ko': ['r2i2p1f2', 'CMIP', 'MIROC6', 'CMIP6Plus', 'amip', 'ACmon', 'gn'],
     'gen_expr_ko': '[MISSING]_ACmon_MIROC6_amip_r2i2p1f2_gn.nc',
     'error_kinds': ['MissingTerm']},

    {'project_id': 'cmip6plus',
     'drs_type': 'datasetid',
     'terms_ok': ['r2i2p1f2', 'CMIP', 'MIROC6', 'CMIP6Plus', 'amip', 'od550aer', 'ACmon', 'gn', 'UA'],
     'gen_expr_ok': 'CMIP6Plus.CMIP.UA.MIROC6.amip.r2i2p1f2.ACmon.od550aer.gn',
     'terms_ko': ['r2i2p1f2', 'CMIP', 'MIROC6', 'CMIP6Plus', 'amip', 'od550aer', 'ACmon', 'gn', 'UA', 'DKRZ'],
     'gen_expr_ko': 'CMIP6Plus.CMIP.[MISSING].MIROC6.amip.r2i2p1f2.ACmon.od550aer.gn',
     'error_kinds': ['TooManyTermsCollection', 'MissingTerm']},
]


def _check_generation(generation_param: dict, is_mapping: bool) -> None:
    if is_mapping:
        url_discriminant = 'mapping'
    else:
        url_discriminant = 'terms'
    url = f"/{generation_param['project_id']}/generation/{url_discriminant}/{generation_param['drs_type']}"
    if is_mapping:
        body = generation_param['mapping_ok']
    else:
        body = generation_param['terms_ok']
    result = _CLIENT.post(url=url, data=json.dumps(body))  # type: ignore
    result.raise_for_status()
    report = DrsGenerationReport(**result.json())
    assert report.validated
    assert report.generated_drs_expression == generation_param['gen_expr_ok']
    if is_mapping:
        body = generation_param['mapping_ko']
    else:
        body = generation_param['terms_ko']
    result = _CLIENT.post(url=url, data=json.dumps(body))  # type: ignore
    result.raise_for_status()
    report = DrsGenerationReport(**result.json())
    assert report.generated_drs_expression == generation_param['gen_expr_ko']
    assert report.nb_errors == len(generation_param['error_kinds'])
    for index in range(0, len(report.errors)):
        assert report.errors[index].kind == generation_param['error_kinds'][index]


def _provide_mapping_generation_params() -> Generator:
    for expression in _SOME_MAPPING_GENERATION_PARAMS:
        yield expression


@pytest.fixture(params=_provide_mapping_generation_params())
def mapping_generation_param(request) -> dict[str, Any]:
    return request.param


def test_mapping_generation(mapping_generation_param) -> None:
    _check_generation(mapping_generation_param, True)


def _provide_terms_generation_params() -> Generator:
    for expression in _SOME_TERMS_GENERATION_PARAMS:
        yield expression


@pytest.fixture(params=_provide_terms_generation_params())
def terms_generation_param(request) -> dict[str, Any]:
    return request.param


def test_terms_generation(terms_generation_param) -> None:
    _check_generation(terms_generation_param, False)
