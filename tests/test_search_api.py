import pytest
from esgvoc.api.search import ItemKind

from esgvoc_backend import search
from tests.api_inputs import (  # noqa: F401
    DEFAULT_COLLECTION,
    DEFAULT_DD,
    DEFAULT_PROJECT,
    find_col_param,
    find_dd_param,
    find_proj_item_param,
    find_term_param,
    find_univ_item_param,
)
from tests.utils import _test_get, client_factory

router = search.router

@pytest.fixture(scope='module')
def client(request):
    return client_factory(request, router)


def test_find_items_in_universe(client, find_univ_item_param) -> None:
    url = '/items/universe'
    params = {'expression': find_univ_item_param.expression}
    select = False
    if find_univ_item_param.item:
        if find_univ_item_param.item_kind == ItemKind.TERM:
            id = find_univ_item_param.item.term_id
            parent_id = find_univ_item_param.item.data_descriptor_id
        else:
            id = find_univ_item_param.item.data_descriptor_id
            parent_id = 'universe'
    else:
        id = None
        parent_id = None
    _test_get(client, url, params, id, select, find_univ_item_param.item_kind, parent_id)


def test_find_items_in_projects(client, find_proj_item_param) -> None:
    url = '/items/projects'
    project_id = find_proj_item_param.item.project_id if find_proj_item_param.item else DEFAULT_PROJECT
    params = {'expression': find_proj_item_param.expression,
              'project_id': project_id}
    select = False
    if find_proj_item_param.item:
        if find_proj_item_param.item_kind == ItemKind.TERM:
            id = find_proj_item_param.item.term_id
            parent_id = find_proj_item_param.item.collection_id
        else:
            id = find_proj_item_param.item.collection_id
            parent_id = find_proj_item_param.item.project_id
    else:
        id = None
        parent_id = None
    _test_get(client, url, params, id, select, find_proj_item_param.item_kind, parent_id)


def test_find_terms_in_universe(client, find_term_param) -> None:
    url = '/terms/universe'
    params = {'expression': find_term_param.expression}
    select = find_term_param.item is not None
    term_id = find_term_param.item.term_id if find_term_param.item else None
    _test_get(client, url, params, term_id, select)


def test_find_terms_in_data_descriptor(client, find_term_param) -> None:
    url = '/terms/universe'
    dd_id = find_term_param.item.data_descriptor_id if find_term_param.item else DEFAULT_DD
    params = {'expression': find_term_param.expression,
              'data_descriptor_id': dd_id}
    select = find_term_param.item is not None
    term_id = find_term_param.item.term_id if find_term_param.item else None
    _test_get(client, url, params, term_id, select)


def test_find_data_descriptors(client, find_dd_param) -> None:
    url = '/data_descriptors'
    params = {'expression': find_dd_param.expression}
    select = False
    dd_id = find_dd_param.item.data_descriptor_id if find_dd_param.item else None
    _test_get(client, url, params, dd_id, select)


def test_find_collections_in_project(client, find_col_param) -> None:
    url = '/collections'
    project_id = find_col_param.item.project_id if find_col_param.item else DEFAULT_PROJECT
    params = {'expression': find_col_param.expression,
              'project_id': project_id}
    select = False
    collection_id = find_col_param.item.collection_id if find_col_param.item else None
    _test_get(client, url, params, collection_id, select)


def test_find_terms_in_project(client, find_term_param) -> None:
    url = '/terms/projects'
    project_id = find_term_param.item.project_id if find_term_param.item else DEFAULT_PROJECT
    params = {'expression': find_term_param.expression,
              'project_id': project_id}
    if find_term_param.item:
        select = True
        term_id = find_term_param.item.term_id
    else:
        select = False
        term_id = None
    _test_get(client, url, params, term_id, select)


def test_find_terms_in_collection(client, find_term_param) -> None:
    url = '/terms/projects'
    project_id = find_term_param.item.project_id if find_term_param.item else DEFAULT_PROJECT
    collection_id = find_term_param.item.collection_id if find_term_param.item else DEFAULT_COLLECTION
    params = {'expression': find_term_param.expression,
              'project_id': project_id,
               'collection_id': collection_id}
    select = find_term_param.item is not None
    term_id = find_term_param.item.term_id if find_term_param.item else None
    _test_get(client, url, params, term_id, select)
