from esgvoc.api.search import ItemKind
from fastapi import FastAPI
from fastapi.testclient import TestClient

from esgvoc_backend import search
from tests.api_inputs import (  # noqa: F401
    find_col_param,
    find_dd_param,
    find_proj_item_param,
    find_term_param,
    find_univ_item_param,
)
from tests.utils import _test_get

_BASE_URL = 'http://localhost:9999/search'

_APP = FastAPI()
_APP.include_router(search.router)
_CLIENT = TestClient(_APP, base_url=_BASE_URL, backend='asyncio')


def test_find_items_in_universe(find_univ_item_param) -> None:
    url = '/items/universe'
    params = {'expression': find_univ_item_param.expression}
    select = False
    if find_univ_item_param.item_kind == ItemKind.TERM:
        id = find_univ_item_param.item.term_id
        parent_id = find_univ_item_param.item.data_descriptor_id
    else:
        id = find_univ_item_param.item.data_descriptor_id
        parent_id = 'universe'
    _test_get(_CLIENT, url, params, id, select, find_univ_item_param.item_kind, parent_id)


def test_find_items_in_projects(find_proj_item_param) -> None:
    url = '/items/projects'
    params = {'expression': find_proj_item_param.expression,
              'project_id': find_proj_item_param.item.project_id}
    select = False
    if find_proj_item_param.item_kind == ItemKind.TERM:
        id = find_proj_item_param.item.term_id
        parent_id = find_proj_item_param.item.collection_id
    else:
        id = find_proj_item_param.item.collection_id
        parent_id = find_proj_item_param.item.project_id
    _test_get(_CLIENT, url, params, id, select, find_proj_item_param.item_kind, parent_id)


def test_find_terms_in_universe(find_term_param) -> None:
    url = '/terms/universe'
    params = {'expression': find_term_param.expression}
    select = True
    _test_get(_CLIENT, url, params, find_term_param.item.term_id, select)


def test_find_terms_in_data_descriptor(find_term_param) -> None:
    url = '/terms/universe'
    params = {'expression': find_term_param.expression,
              'data_descriptor_id': find_term_param.item.data_descriptor_id}
    select = True
    _test_get(_CLIENT, url, params, find_term_param.item.term_id, select)


def test_find_data_descriptors(find_dd_param) -> None:
    url = '/data_descriptors'
    params = {'expression': find_dd_param.expression}
    select = False
    _test_get(_CLIENT, url, params, find_dd_param.item.data_descriptor_id, select)


def test_find_collections_in_project(find_col_param) -> None:
    url = '/collections'
    params = {'expression': find_col_param.expression,
              'project_id': find_col_param.item.project_id}
    select = False
    _test_get(_CLIENT, url, params, find_col_param.item.collection_id, select)


def test_find_terms_in_project(find_term_param) -> None:
    url = '/terms/projects'
    params = {'expression': find_term_param.expression,
              'project_id': find_term_param.item.project_id}
    select = True
    _test_get(_CLIENT, url, params, find_term_param.item.term_id, select)


def test_find_terms_in_collection(find_term_param) -> None:
    url = '/terms/projects'
    params = {'expression': find_term_param.expression,
              'project_id': find_term_param.item.project_id,
               'collection_id': find_term_param.item.collection_id}
    select = True
    _test_get(_CLIENT, url, params, find_term_param.item.term_id, select)
