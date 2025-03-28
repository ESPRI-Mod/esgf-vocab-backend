from fastapi import FastAPI
from fastapi.testclient import TestClient

from esgvoc_backend import cross
from tests.utils import _test_get

_BASE_URL = 'http://localhost:9999/cross'

_APP = FastAPI()
_APP.include_router(cross.router)
_CLIENT = TestClient(_APP, base_url=_BASE_URL, backend='asyncio')

# TODO: add parameters.


def test_cross_term_in_all_projects() -> None:
    url = '/terms'
    universe_term_id = 'ipsl'
    data_descriptor_id = 'organisation'
    params = {'data_descriptor_id': data_descriptor_id, 'universe_term_id': universe_term_id}
    min_items = 2
    select = True
    _test_get(_CLIENT, url, params, min_items, universe_term_id, select)


def test_cross_term_in_project() -> None:
    url = '/terms'
    universe_term_id = 'ipsl'
    data_descriptor_id = 'organisation'
    project_id = 'cmip6'
    params = {'project_id': project_id, 'data_descriptor_id': data_descriptor_id,
              'universe_term_id': universe_term_id}
    min_items = 1
    select = True
    _test_get(_CLIENT, url, params, min_items, universe_term_id, select)


def test_cross_collection_in_all_projects() -> None:
    url = '/collections'
    collection_id = 'institution_id'
    data_descriptor_id = 'organisation'
    params = {'data_descriptor_id': data_descriptor_id}
    min_items = 2
    select = False
    _test_get(_CLIENT, url, params, min_items, collection_id, select)


def test_cross_collection_in_project() -> None:
    url = '/collections'
    collection_id = 'institution_id'
    data_descriptor_id = 'organisation'
    project_id = 'cmip6'
    params = {'data_descriptor_id': data_descriptor_id, 'project_id': project_id}
    min_items = 1
    select = False
    _test_get(_CLIENT, url, params, min_items, collection_id, select)
