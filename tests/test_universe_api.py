import json

from fastapi import FastAPI
from fastapi.testclient import TestClient

from esgvoc_backend.universe import router

_BASE_URL = 'http://localhost:9999/universe'

app = FastAPI()
app.include_router(router)
client = TestClient(app, base_url=_BASE_URL, backend='asyncio')


def _test_get(url: str, min_items: int, select: bool):
    result = client.get(url=url)
    result.raise_for_status()
    assert len(result.json()) > min_items
    if select:
        params = {'selected_term_fields': ['drs_name']}
        result = client.get(url=url, params=params)
        result = result.json()
        assert len(result) > min_items
        assert len(result[min_items]) == 3


def _test_find(url: str, params: dict[str: str], select: bool):
    settings = {'case_sensitive': False, 'selected_term_fields': ['drs_name']}
    result = client.post(url=url, params=params)
    result.raise_for_status()
    assert len(result.json()) == 0
    result = client.post(url=url, params=params, data=json.dumps(settings))
    result.raise_for_status()
    result = result.json()
    assert len(result) == 1
    if select:
        assert len(result[0]) == 3


def test_terms_in_universe_get() -> None:
    url = '/terms'
    min_items = 2000
    _test_get(url, min_items, True)


def test_terms_in_universe_find() -> None:
    url = '/terms/find'
    params = {'term_id': 'IpsL'}
    _test_find(url, params, True)


def test_data_descriptors_get():
    url = '/data_descriptors'
    min_items = 10
    _test_get(url, min_items, False)


def test_data_descriptors_find() -> None:
    url = '/data_descriptors/find'
    params = {'data_descriptor_id': 'InstitutioN'}
    _test_find(url, params, False)


def test_terms_in_data_descriptor_get() -> None:
    data_descriptor_id = 'institution'
    url = f'/data_descriptors/{data_descriptor_id}/terms'
    min_items = 10
    _test_get(url, min_items, True)


def test_terms_in_data_descriptor_find() -> None:
    data_descriptor_id = 'institution'
    url = f'/data_descriptors/{data_descriptor_id}/terms/find'
    params = {'term_id': 'IpsL'}
    _test_find(url, params, True)
