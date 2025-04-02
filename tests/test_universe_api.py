from fastapi import FastAPI
from fastapi.testclient import TestClient

from esgvoc_backend import universe
from tests.api_inputs import get_param  # noqa: F401
from tests.utils import _test_get

_BASE_URL = 'http://localhost:9999/universe'

_APP = FastAPI()
_APP.include_router(universe.router)
_CLIENT = TestClient(_APP, base_url=_BASE_URL, backend='asyncio')


def test_get_terms_in_universe(get_param) -> None:
    url = '/terms'
    params = None
    select = True
    _test_get(_CLIENT, url, params, get_param.term_id, select)


def test_get_term_in_universe(get_param) -> None:
    url = f'/terms/{get_param.term_id}'
    params = None
    select = True
    _test_get(_CLIENT, url, params, get_param.term_id, select)


def test_get_data_descriptors(get_param):
    url = '/data_descriptors'
    params = None
    select = False
    _test_get(_CLIENT, url, params, get_param.data_descriptor_id, select)


def test_get_data_descriptor(get_param):
    url = f'/data_descriptors/{get_param.data_descriptor_id}'
    params = None
    select = False
    _test_get(_CLIENT, url, params, get_param.data_descriptor_id, select)


def test_get_terms_in_data_descriptor(get_param) -> None:
    url = f'/data_descriptors/{get_param.data_descriptor_id}/terms'
    params = None
    select = True
    _test_get(_CLIENT, url, params, get_param.term_id, select)


def test_get_term_in_data_descriptor(get_param) -> None:
    url = f'/data_descriptors/{get_param.data_descriptor_id}/terms/{get_param.term_id}'
    params = None
    select = True
    _test_get(_CLIENT, url, params, get_param.term_id, select)
