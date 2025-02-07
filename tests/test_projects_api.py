from fastapi import FastAPI
from fastapi.testclient import TestClient

import esgvoc_backend.projects as projects
from tests.test_universe_api import _test_find, _test_get

_BASE_URL = 'http://localhost:9999/projects'


_APP = FastAPI()
_APP.include_router(projects.router)
_CLIENT = TestClient(_APP, base_url=_BASE_URL, backend='asyncio')


def _test_validation(client: TestClient, url: str, params: list[dict],
                     nb_results:int = 1, has_report: bool = False):
    results = client.get(url=url, params=params[0])
    results.raise_for_status()
    results = results.json()
    if has_report:
        assert not results['validated']
    else:
        assert len(results) == 0
    results = client.get(url=url, params=params[1])
    results.raise_for_status()
    results = results.json()
    if has_report:
        assert results['validated']
    else:
        assert len(results) == nb_results
        for result in results:
            assert result['term_id'] == params[1]['value'].lower()


def test_get_projects() -> None:
    url = '/'
    min_items = 2
    select = False
    _test_get(client=_CLIENT, url=url, min_items=min_items, select=select)


def test_find_projects() -> None:
    url = '/find'
    params = {'project_id': 'cmip6'}
    result = _CLIENT.get(url=url, params=params)
    result.raise_for_status()
    assert len(result.json()) >= 2


def test_get_all_terms_all_projects() -> None:
    url = '/terms'
    min_items = 2000
    select = True
    _test_get(client=_CLIENT, url=url, min_items=min_items, select=select)


def test_find_terms_all_projects() -> None:
    url = '/terms/find'
    params = {'term_id': 'ACABf'}
    select = True
    nb_results = 2
    _test_find(client=_CLIENT, url=url, params=params, select=select, nb_results=nb_results)


def test_valid_term_all_projects() -> None:
    url = '/terms/valid'
    params = [{'value': 'IpsL'}, {'value': 'IPSL'}]
    _test_validation(client=_CLIENT, url=url, params=params, nb_results=2)


def test_cross_all_projects() -> None:
    url = '/terms/cross'
    params = {'data_descriptor_id': 'organisation', 'term_id': 'IpsL'}
    _test_find(client=_CLIENT, url=url, params=params, select=True, nb_results=2, level=4)


def test_get_all_terms_in_project() -> None:
    url = '/cmip6/terms'
    min_items = 100
    select = True
    _test_get(client=_CLIENT, url=url, min_items=min_items, select=select)


def test_find_terms_in_project() -> None:
    url = '/cmip6/terms/find'
    params = {'term_id': 'IpsL'}
    select = True
    nb_results = 1
    _test_find(client=_CLIENT, url=url, params=params, select=select, nb_results=nb_results)


def test_valid_term_in_project() -> None:
    url = '/cmip6/terms/valid'
    params = [{'value': 'IpsL'}, {'value': 'IPSL'}]
    _test_validation(client=_CLIENT, url=url, params=params, nb_results=1)


def test_cross_in_project() -> None:
    url = '/cmip6/terms/cross'
    params = {'data_descriptor_id': 'organisation', 'term_id': 'IpsL'}
    _test_find(client=_CLIENT, url=url, params=params, select=True, nb_results=1, level=2)


def test_get_collections_in_project() -> None:
    url = '/cmip6/collections'
    min_items = 10
    select = False
    _test_get(client=_CLIENT, url=url, min_items=min_items, select=select)


def test_find_collections_in_project() -> None:
    url = '/cmip6/collections/find'
    params = {'collection_id': 'Institution_ID'}
    select = False
    nb_results = 1
    _test_find(client=_CLIENT, url=url, params=params, select=select, nb_results=nb_results)


def test_get_all_terms_in_collection() -> None:
    url = '/cmip6/collections/institution_id/terms'
    min_items = 20
    select = True
    _test_get(client=_CLIENT, url=url, min_items=min_items, select=select)


def test_find_terms_in_collection() -> None:
    url = '/cmip6/collections/institution_id/terms/find'
    params = {'term_id': 'IpsL'}
    select = True
    _test_find(client=_CLIENT, url=url, params=params, select=select)


def test_valid_term_in_collection() -> None:
    url = '/cmip6/collections/institution_id/terms/valid'
    params = [{'value': 'IpsL'}, {'value': 'IPSL'}]
    _test_validation(client=_CLIENT, url=url, params=params, nb_results=1)


def test_valid_term() -> None:
    url = '/cmip6/collections/institution_id/terms/valid'
    params = [{'value': 'IpsL', 'term_id': 'ipsl'}, {'value': 'IPSL', 'term_id': 'ipsl'}]
    _test_validation(client=_CLIENT, url=url, params=params, has_report=True)
