from fastapi import FastAPI
from fastapi.testclient import TestClient

from esgvoc_backend import validation

_BASE_URL = 'http://localhost:9999/validation'

_APP = FastAPI()
_APP.include_router(validation.router)
_CLIENT = TestClient(_APP, base_url=_BASE_URL, backend='asyncio')

# TODO: add parameters.


def _test_validation(client: TestClient, url: str, params: list[dict],
                     nb_results: int = 1, has_report: bool = False) -> None:
    results = client.get(url=url, params=params[0])
    results.raise_for_status()
    json_results = results.json()
    if has_report:
        assert not json_results['validated']
    else:
        assert len(json_results) == 0
    results = client.get(url=url, params=params[1])
    results.raise_for_status()
    json_results = results.json()
    if has_report:
        assert json_results['validated']
    else:
        assert len(json_results) == nb_results
        for result in json_results:
            assert result['term_id'] == params[1]['value'].lower()


def test_valid_term_all_projects() -> None:
    url = '/terms'
    params = [{'value': 'IpsL'}, {'value': 'IPSL'}]
    _test_validation(client=_CLIENT, url=url, params=params, nb_results=2)


def test_valid_term_in_project() -> None:
    url = '/terms'
    params = [{'value': 'IpsL', 'project_id': 'cmip6'}, {'value': 'IPSL', 'project_id': 'cmip6'}]
    _test_validation(client=_CLIENT, url=url, params=params, nb_results=1)


def test_valid_term_in_collection() -> None:
    url = '/terms'
    params = [{'value': 'IpsL', 'project_id': 'cmip6', 'collection_id': 'institution_id'},
              {'value': 'IPSL', 'project_id': 'cmip6', 'collection_id': 'institution_id'}]
    _test_validation(client=_CLIENT, url=url, params=params, nb_results=1)


def test_valid_term() -> None:
    url = '/terms'
    params = [{'value': 'IpsL', 'project_id': 'cmip6', 'collection_id': 'institution_id', 'term_id': 'ipsl'},
              {'value': 'IPSL', 'project_id': 'cmip6', 'collection_id': 'institution_id', 'term_id': 'ipsl'}]
    _test_validation(client=_CLIENT, url=url, params=params, has_report=True)
