from fastapi import FastAPI
from fastapi.testclient import TestClient

from esgvoc_backend import projects
from tests.utils import _test_get, proj_dd_col_term_id, project_id  # noqa: F401

_BASE_URL = 'http://localhost:9999/projects'

_APP = FastAPI()
_APP.include_router(projects.router)
_CLIENT = TestClient(_APP, base_url=_BASE_URL, backend='asyncio')


def test_get_projects(project_id) -> None:  # noqa: F811
    url = '/'
    params = None
    min_items = 2
    select = False
    _test_get(_CLIENT, url, params, min_items, project_id, select)


def test_get_project(project_id) -> None:  # noqa: F811
    url = f'/{project_id}'
    params = None
    min_items = 1
    select = False
    _test_get(_CLIENT, url, params, min_items, project_id, select)


def test_get_all_terms_in_project(proj_dd_col_term_id) -> None:  # noqa: F811
    url = f'/{proj_dd_col_term_id[0]}/terms'
    params = None
    min_items = 100
    select = True
    _test_get(_CLIENT, url, params, min_items, proj_dd_col_term_id[3], select)


def test_get_collections_in_project(proj_dd_col_term_id) -> None:  # noqa: F811
    url = f'/{proj_dd_col_term_id[0]}/collections'
    params = None
    min_items = 10
    select = False
    _test_get(_CLIENT, url, params, min_items, proj_dd_col_term_id[2], select)


def test_get_all_terms_in_collection(proj_dd_col_term_id) -> None:  # noqa: F811
    url = f'/{proj_dd_col_term_id[0]}/collections/{proj_dd_col_term_id[2]}/terms'
    params = None
    min_items = 3
    select = True
    _test_get(_CLIENT, url, params, min_items, proj_dd_col_term_id[3], select)


def test_get_term_in_project(proj_dd_col_term_id) -> None:  # noqa: F811
    url = f'/{proj_dd_col_term_id[0]}/terms/{proj_dd_col_term_id[3]}'
    params = None
    min_items = 1
    select = True
    _test_get(_CLIENT, url, params, min_items, proj_dd_col_term_id[3], select)


def test_get_term_in_collection(proj_dd_col_term_id) -> None:  # noqa: F811
    url = f'/{proj_dd_col_term_id[0]}/collections/{proj_dd_col_term_id[2]}/terms/{proj_dd_col_term_id[3]}'
    params = None
    min_items = 1
    select = True
    _test_get(_CLIENT, url, params, min_items, proj_dd_col_term_id[3], select)


def test_get_collection_in_project(proj_dd_col_term_id) -> None:  # noqa: F811
    url = f'/{proj_dd_col_term_id[0]}/collections/{proj_dd_col_term_id[2]}'
    params = None
    min_items = 1
    select = False
    _test_get(_CLIENT, url, params, min_items, proj_dd_col_term_id[2], select)
