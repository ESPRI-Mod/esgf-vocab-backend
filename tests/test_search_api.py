from fastapi import FastAPI
from fastapi.testclient import TestClient

from esgvoc_backend import search
from tests.utils import _test_get

_BASE_URL = 'http://localhost:9999/search'

_APP = FastAPI()
_APP.include_router(search.router)
_CLIENT = TestClient(_APP, base_url=_BASE_URL, backend='asyncio')
_PROJECT_ID = 'cmip6'

# TODO: add parameters.


def test_find_items_in_universe() -> None:
    url = '/items/universe'
    id = 'ipsl'
    params = {'expression': 'Paris NOT CNES'}
    min_items = 2
    select = False
    _test_get(_CLIENT, url, params, min_items, id, select)


def test_find_items_in_projects() -> None:
    url = '/items/projects'
    id = 'ipsl'
    params = {'expression': 'Paris NOT CNES', 'project_id': _PROJECT_ID}
    min_items = 1
    select = False
    _test_get(_CLIENT, url, params, min_items, id, select)


def test_find_terms_in_universe() -> None:
    url = '/terms/universe'
    id = 'ipsl'
    params = {'expression': 'IpsL', 'only_id': True}
    min_items = 2
    select = True
    _test_get(_CLIENT, url, params, min_items, id, select)


def test_find_terms_in_data_descriptor() -> None:
    data_descriptor_id = 'institution'
    url = '/terms/universe'
    term_id = 'ipsl'
    params = {'expression': 'IpsL NOT CNES', 'data_descriptor_id': data_descriptor_id}
    min_items = 1
    select = True
    _test_get(_CLIENT, url, params, min_items, term_id, select)


def test_find_data_descriptors() -> None:
    url = '/data_descriptors'
    data_descriptor_id = 'institution'
    params = {'expression': 'Instit*'}
    min_items = 1
    select = False
    _test_get(_CLIENT, url, params, min_items, data_descriptor_id, select)


def test_find_collections_in_project() -> None:
    project_id = 'cmip6'
    expression = 'instit*'
    collection_id = 'institution_id'
    url = 'collections'
    params = {'expression': expression, 'project_id': project_id}
    select = False
    min_items = 1
    _test_get(_CLIENT, url, params, min_items, collection_id, select)


def test_find_terms_in_project() -> None:
    url = '/terms/projects'
    params = {'expression': 'ACABf', 'project_id': 'cmip6'}
    term_id = 'acabf'
    min_items = 1
    select = True
    _test_get(_CLIENT, url, params, min_items, term_id, select)


def test_find_terms_in_collection() -> None:
    url = '/terms/projects'
    params = {'expression': 'ipsl', 'project_id': 'cmip6', 'collection_id': 'institution_id'}
    term_id = 'ipsl'
    min_items = 1
    select = True
    _test_get(_CLIENT, url, params, min_items, term_id, select)
