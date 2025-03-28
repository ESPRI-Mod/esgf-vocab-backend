from fastapi import FastAPI
from fastapi.testclient import TestClient

from esgvoc_backend import universe
from tests.utils import _test_get, data_descriptor_id, dd_term_ids, term_id  # noqa: F401

_BASE_URL = 'http://localhost:9999/universe'

_APP = FastAPI()
_APP.include_router(universe.router)
_CLIENT = TestClient(_APP, base_url=_BASE_URL, backend='asyncio')


def test_get_terms_in_universe(term_id) -> None:  # noqa: F811
    url = '/terms'
    params = None
    min_items = 2000
    select = True
    _test_get(_CLIENT, url, params, min_items, term_id, select)


def test_get_term_in_universe(term_id) -> None:  # noqa: F811
    url = f'/terms/{term_id}'
    params = None
    min_items = 1
    select = True
    _test_get(_CLIENT, url, params, min_items, term_id, select)


def test_get_data_descriptors(data_descriptor_id):  # noqa: F811
    url = '/data_descriptors'
    params = None
    min_items = 10
    select = False
    _test_get(_CLIENT, url, params, min_items, data_descriptor_id, select)


def test_get_data_descriptor(data_descriptor_id):  # noqa: F811
    url = f'/data_descriptors/{data_descriptor_id}'
    params = None
    min_items = 1
    select = False
    _test_get(_CLIENT, url, params, min_items, data_descriptor_id, select)


def test_get_terms_in_data_descriptor(dd_term_ids) -> None:  # noqa: F811
    url = f'/data_descriptors/{dd_term_ids[0]}/terms'
    params = None
    min_items = 3
    select = True
    _test_get(_CLIENT, url, params, min_items, dd_term_ids[1], select)


def test_get_term_in_data_descriptor(dd_term_ids) -> None:  # noqa: F811
    url = f'/data_descriptors/{dd_term_ids[0]}/terms/{dd_term_ids[1]}'
    params = None
    min_items = 1
    select = True
    _test_get(_CLIENT, url, params, min_items, dd_term_ids[1], select)
