from fastapi import FastAPI
from fastapi.testclient import TestClient

from esgvoc_backend import projects
from tests.api_inputs import get_param  # noqa: F401
from tests.utils import _test_get

_BASE_URL = 'http://localhost:9999/projects'

_APP = FastAPI()
_APP.include_router(projects.router)
_CLIENT = TestClient(_APP, base_url=_BASE_URL, backend='asyncio')


def test_get_projects(get_param) -> None:
    url = '/'
    params = None
    select = False
    _test_get(_CLIENT, url, params, get_param.project_id, select)


def test_get_project(get_param) -> None:
    url = f'/{get_param.project_id}'
    params = None
    select = False
    _test_get(_CLIENT, url, params, get_param.project_id, select)


def test_get_all_terms_in_project(get_param) -> None:
    url = f'/{get_param.project_id}/terms'
    params = None
    select = True
    _test_get(_CLIENT, url, params, get_param.term_id, select)


def test_get_collections_in_project(get_param) -> None:
    url = f'/{get_param.project_id}/collections'
    params = None
    select = False
    _test_get(_CLIENT, url, params, get_param.collection_id, select)


def test_get_all_terms_in_collection(get_param) -> None:
    url = f'/{get_param.project_id}/collections/{get_param.collection_id}/terms'
    params = None
    select = True
    _test_get(_CLIENT, url, params, get_param.term_id, select)


def test_get_term_in_project(get_param) -> None:
    url = f'/{get_param.project_id}/terms/{get_param.term_id}'
    params = None
    select = True
    _test_get(_CLIENT, url, params, get_param.term_id, select)


def test_get_term_in_collection(get_param) -> None:
    url = f'/{get_param.project_id}/collections/{get_param.collection_id}/terms/{get_param.term_id}'
    params = None
    select = True
    _test_get(_CLIENT, url, params, get_param.term_id, select)


def test_get_collection_in_project(get_param) -> None:
    url = f'/{get_param.project_id}/collections/{get_param.collection_id}'
    params = None
    select = False
    _test_get(_CLIENT, url, params, get_param.collection_id, select)
