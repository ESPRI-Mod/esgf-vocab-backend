import json

from fastapi import FastAPI
from fastapi.testclient import TestClient

import esgvoc_backend.universe as universe

_BASE_URL = 'http://localhost:9999/universe'

_APP = FastAPI()
_APP.include_router(universe.router)
_CLIENT = TestClient(_APP, base_url=_BASE_URL, backend='asyncio')


def _test_get(client: TestClient, url: str, min_items: int, select: bool):
    result = client.get(url=url)
    result.raise_for_status()
    assert len(result.json()) >= min_items
    if select:
        params = {'selected_term_fields': ['drs_name']}
        result = client.get(url=url, params=params)
        result = result.json()
        assert len(result) >= min_items
        assert len(result[min_items]) == 3


def _test_find(client: TestClient, url: str, params: dict[str: str], select: bool,
               nb_results: int = 1, level: int = 1):
    settings = {'case_sensitive': False, 'selected_term_fields': ['drs_name']}
    result = client.post(url=url, params=params)
    result.raise_for_status()
    assert len(result.json()) == 0
    result = client.post(url=url, params=params, data=json.dumps(settings))
    result.raise_for_status()
    result = result.json()
    assert len(result) == nb_results
    if select:
        data = result
        for _ in range(0, level):
            data = data[0]
        assert len(data) == 3


def test_get_terms_in_universe() -> None:
    url = '/terms'
    min_items = 2000
    _test_get(_CLIENT, url, min_items, True)


def test_find_terms_in_universe() -> None:
    url = '/terms/find'
    params = {'term_id': 'IpsL'}
    _test_find(_CLIENT, url, params, True)


def test_get_data_descriptors():
    url = '/data_descriptors'
    min_items = 10
    _test_get(_CLIENT, url, min_items, False)


def test_find_data_descriptors() -> None:
    url = '/data_descriptors/find'
    params = {'data_descriptor_id': 'InstitutioN'}
    _test_find(_CLIENT, url, params, False)


def test_get_terms_in_data_descriptor() -> None:
    data_descriptor_id = 'institution'
    url = f'/data_descriptors/{data_descriptor_id}/terms'
    min_items = 10
    _test_get(_CLIENT, url, min_items, True)


def test_find_terms_in_data_descriptor() -> None:
    data_descriptor_id = 'institution'
    url = f'/data_descriptors/{data_descriptor_id}/terms/find'
    params = {'term_id': 'IpsL'}
    _test_find(_CLIENT, url, params, True)
