from fastapi import FastAPI
from fastapi.testclient import TestClient

import esgvoc_backend.universe as universe

_BASE_URL = 'http://localhost:9999/universe'

_APP = FastAPI()
_APP.include_router(universe.router)
_CLIENT = TestClient(_APP, base_url=_BASE_URL, backend='asyncio')
_SELECT = {'selected_term_fields': ['drs_name']}


def _test_get(client: TestClient, url: str, params: dict | None, min_items: int, select: bool) -> None:
    result = client.get(url=url, params=params)
    result.raise_for_status()
    if min_items > 0:
        json_result = result.json()
        assert json_result is not None
        assert len(json_result) >= min_items
        print(json_result)
        if select:
            if params:
                params.update(_SELECT)
            else:
                params = _SELECT
            result = client.get(url=url, params=params)
            json_result = result.json()
            assert len(json_result) >= min_items
            if isinstance(json_result, list):
                assert len(json_result[min_items-1]) == 3
            else:
                assert len(json_result) == 3
    else:
        assert result.json() is None


def test_find_items_in_universe() -> None:
    url = '/items/find'
    params = {'expression': 'ipsl', 'only_id': True}
    min_items = 1
    select = False
    _test_get(_CLIENT, url, params, min_items, select)


def test_get_terms_in_universe() -> None:
    url = '/terms'
    params = None
    min_items = 2000
    select = True
    _test_get(_CLIENT, url, params, min_items, select)


def test_get_term_in_universe() -> None:
    term_id = 'ipsl'
    url = '/terms/get'
    params = {'term_id': term_id}
    min_items = 1
    select = True
    _test_get(_CLIENT, url, params, min_items, select)


def test_find_terms_in_universe() -> None:
    url = '/terms/find'
    params = {'expression': 'IpsL'}
    min_items = 2
    select = True
    _test_get(_CLIENT, url, params, min_items, select)


def test_get_data_descriptors():
    url = '/data_descriptors'
    params = None
    min_items = 10
    select = False
    _test_get(_CLIENT, url, params, min_items, select)


def test_get_data_descriptor():
    data_descriptor_id = 'institution'
    url = '/data_descriptors/get'
    params = {'data_descriptor_id': data_descriptor_id}
    min_items = 1
    select = False
    _test_get(_CLIENT, url, params, min_items, select)


def test_find_data_descriptors() -> None:
    url = '/data_descriptors/find'
    params = {'expression': 'InstitutioN'}
    min_items = 1
    select = False
    _test_get(_CLIENT, url, params, min_items, select)


def test_get_terms_in_data_descriptor() -> None:
    data_descriptor_id = 'institution'
    url = f'/data_descriptors/{data_descriptor_id}/terms'
    params = None
    min_items = 10
    select = True
    _test_get(_CLIENT, url, params, min_items, select)


def test_get_term_in_data_descriptor() -> None:
    data_descriptor_id = 'institution'
    term_id = 'ipsl'
    url = f'/data_descriptors/{data_descriptor_id}/terms/get'
    params = {'term_id': term_id}
    min_items = 1
    select = True
    _test_get(_CLIENT, url, params, min_items, select)


def test_find_terms_in_data_descriptor() -> None:
    data_descriptor_id = 'institution'
    url = f'/data_descriptors/{data_descriptor_id}/terms/find'
    params = {'expression': 'IpsL NOT CNES'}
    min_items = 1
    select = True
    _test_get(_CLIENT, url, params, min_items, select)
