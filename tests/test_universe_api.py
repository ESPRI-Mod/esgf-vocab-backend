import json

import requests as r

_BASE_URL = 'http://localhost:9999/universe'


def _test_get(url: str, min_items: int, select: bool):
    result = r.get(url=url)
    result.raise_for_status()
    assert len(result.json()) > min_items
    if select:
        params = {'selected_term_fields': ['drs_name']}
        result = r.get(url=url, params=params)
        result = result.json()
        assert len(result) > min_items
        assert len(result[min_items]) == 3


def _test_find(url: str, params: dict[str: str], select: bool):
    settings = {'case_sensitive': False, 'selected_term_fields': ['drs_name']}
    result = r.get(url=url, params=params)
    result.raise_for_status()
    assert len(result.json()) == 0
    result = r.get(url=url, params=params, data=json.dumps(settings))
    result.raise_for_status()
    result = result.json()
    assert len(result) == 1
    if select:
        assert len(result[0]) == 3


def test_terms_in_universe_get() -> None:
    url = _BASE_URL + '/terms'
    min_items = 2000
    _test_get(url, min_items, True)


def test_terms_in_universe_find() -> None:
    url = _BASE_URL + '/terms/find'
    params = {'term_id': 'IpsL'}
    _test_find(url, params, True)


def test_data_descriptors_get():
    url = _BASE_URL + '/data_descriptors'
    min_items = 10
    _test_get(url, min_items, False)


def test_data_descriptors_find() -> None:
    url = _BASE_URL + '/data_descriptors/find'
    params = {'data_descriptor_id': 'InstitutioN'}
    _test_find(url, params, False)


def test_terms_in_data_descriptor_get() -> None:
    data_descriptor_id = 'institution'
    url = _BASE_URL + f'/data_descriptors/{data_descriptor_id}/terms'
    min_items = 10
    _test_get(url, min_items, True)


def test_terms_in_data_descriptor_find() -> None:
    data_descriptor_id = 'institution'
    url = _BASE_URL + f'/data_descriptors/{data_descriptor_id}/terms/find'
    params = {'term_id': 'IpsL'}
    _test_find(url, params, True)
