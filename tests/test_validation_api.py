from typing import cast

from esgvoc.api.report import ValidationReport
from esgvoc.api.search import MatchingTerm
from fastapi import FastAPI
from fastapi.testclient import TestClient

from esgvoc_backend import validation
from tests.api_inputs import LEN_PROJECTS, ValidationExpression, check_validation, val_query  # noqa: F401
from tests.utils import instantiate

_BASE_URL = 'http://localhost:9999/validation'

_APP = FastAPI()
_APP.include_router(validation.router)
_CLIENT = TestClient(_APP, base_url=_BASE_URL, backend='asyncio')


def _test_validation(client: TestClient, url: str, params: dict, query: ValidationExpression) -> None:
    results = client.get(url=url, params=params)
    results.raise_for_status()
    json_results = results.json()
    matching_terms = instantiate(json_results)
    if matching_terms is None:
        matching_terms = list()
    elif not isinstance(matching_terms, list):
        matching_terms = [matching_terms]
    check_validation(query, cast(list[MatchingTerm], matching_terms))


def test_valid_term_all_projects(val_query) -> None:
    url = '/terms'
    params = {'value': val_query.value}
    query = ValidationExpression(value=val_query.value, item=val_query.item,
                                 nb_matching_terms=val_query.nb_matching_terms*LEN_PROJECTS,
                                 nb_errors=val_query.nb_errors)
    _test_validation(client=_CLIENT, url=url, params=params, query=query)


def test_valid_term_in_project(val_query) -> None:
    url = '/terms'
    params = {'value': val_query.value, 'project_id': val_query.item.project_id}
    _test_validation(client=_CLIENT, url=url, params=params, query=val_query)


def test_valid_term_in_collection(val_query) -> None:
    url = '/terms'
    params = {'value': val_query.value, 'project_id': val_query.item.project_id,
              'collection_id': val_query.item.collection_id}
    _test_validation(client=_CLIENT, url=url, params=params, query=val_query)


def test_valid_term(val_query) -> None:
    url = '/terms'
    params = {'value': val_query.value, 'project_id': val_query.item.project_id,
              'collection_id': val_query.item.collection_id, 'term_id': val_query.item.term_id}
    results = _CLIENT.get(url=url, params=params)
    results.raise_for_status()
    json_results = results.json()
    report = ValidationReport(**json_results)
    assert val_query.nb_errors == len(report.errors)
