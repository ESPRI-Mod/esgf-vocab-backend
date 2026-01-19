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
from tests.utils import client_factory

router = search.router

@pytest.fixture(scope='module')
def client(request):
    return client_factory(request, router)


def test_find_items_in_universe(client, find_univ_item_param) -> None:
    """Test /search/items/universe endpoint."""
    url = '/items/universe'
    params = {'expression': find_univ_item_param.expression}

    response = client.get(url=url, params=params)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)

    # If we expect results, validate them
    if find_univ_item_param.item:
        assert len(json_result) > 0
        # Each item should have kind, id, parent_id
        for item in json_result:
            assert isinstance(item, dict)
            assert 'kind' in item
            assert 'id' in item
            assert 'parent_id' in item


def test_find_items_in_projects(client, find_proj_item_param) -> None:
    """Test /search/items/projects endpoint."""
    url = '/items/projects'
    project_id = find_proj_item_param.item.project_id if find_proj_item_param.item else DEFAULT_PROJECT
    params = {'expression': find_proj_item_param.expression,
              'project_id': project_id}

    response = client.get(url=url, params=params)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)

    # If we expect results, validate them
    if find_proj_item_param.item:
        assert len(json_result) > 0
        # Each item should have kind, id, parent_id
        for item in json_result:
            assert isinstance(item, dict)
            assert 'kind' in item
            assert 'id' in item
            assert 'parent_id' in item


def test_find_terms_in_universe(client, find_term_param) -> None:
    """Test /search/terms/universe endpoint."""
    url = '/terms/universe'
    params = {'expression': find_term_param.expression}

    # Test basic request
    response = client.get(url=url, params=params)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)

    # If we expect specific term, validate it
    if find_term_param.item:
        assert len(json_result) > 0
        for term in json_result:
            assert isinstance(term, dict)
            assert 'id' in term
            assert 'type' in term

        # Test with selected_term_fields
        params_with_select = params.copy()
        params_with_select['selected_term_fields'] = ['drs_name', 'nothing']

        response = client.get(url=url, params=params_with_select)
        assert response.status_code == 200

        json_result = response.json()
        for term in json_result:
            # With new behavior: only 'id' + selected fields that exist
            assert 'id' in term
            # 'nothing' should not be included (invalid field)
            assert 'nothing' not in term
            # 'type' and 'description' are NOT included when selected_term_fields is used


def test_find_terms_in_data_descriptor(client, find_term_param) -> None:
    """Test /search/terms/universe with data_descriptor_id filter."""
    url = '/terms/universe'
    dd_id = find_term_param.item.data_descriptor_id if find_term_param.item else DEFAULT_DD
    params = {'expression': find_term_param.expression,
              'data_descriptor_id': dd_id}

    # Test basic request
    response = client.get(url=url, params=params)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)

    # If we expect specific term, validate it
    if find_term_param.item:
        assert len(json_result) > 0
        for term in json_result:
            assert isinstance(term, dict)
            assert 'id' in term
            assert 'type' in term

        # Test with selected_term_fields
        params_with_select = params.copy()
        params_with_select['selected_term_fields'] = ['drs_name', 'nothing']

        response = client.get(url=url, params=params_with_select)
        assert response.status_code == 200

        json_result = response.json()
        for term in json_result:
            # With new behavior: only 'id' + selected fields that exist
            assert 'id' in term
            # 'nothing' should not be included (invalid field)
            assert 'nothing' not in term
            # 'type' and 'description' are NOT included when selected_term_fields is used


def test_find_data_descriptors(client, find_dd_param) -> None:
    """Test /search/data_descriptors endpoint."""
    url = '/data_descriptors'
    params = {'expression': find_dd_param.expression}

    response = client.get(url=url, params=params)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)

    # If we expect specific data descriptor, check it's in results
    # Results are returned as [[id, context], ...], so extract the IDs
    if find_dd_param.item:
        assert len(json_result) > 0
        # Extract just the IDs from [id, context] tuples
        result_ids = [item[0] if isinstance(item, list) else item for item in json_result]
        assert find_dd_param.item.data_descriptor_id in result_ids


def test_find_collections_in_project(client, find_col_param) -> None:
    """Test /search/collections endpoint."""
    url = '/collections'
    project_id = find_col_param.item.project_id if find_col_param.item else DEFAULT_PROJECT
    params = {'expression': find_col_param.expression,
              'project_id': project_id}

    response = client.get(url=url, params=params)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)

    # If we expect specific collection, check it's in results
    # Results are returned as [[id, context], ...], so extract the IDs
    if find_col_param.item:
        assert len(json_result) > 0
        # Extract just the IDs from [id, context] tuples
        result_ids = [item[0] if isinstance(item, list) else item for item in json_result]
        assert find_col_param.item.collection_id in result_ids


def test_find_terms_in_project(client, find_term_param) -> None:
    """Test /search/terms/projects endpoint."""
    url = '/terms/projects'
    project_id = find_term_param.item.project_id if find_term_param.item else DEFAULT_PROJECT
    params = {'expression': find_term_param.expression,
              'project_id': project_id}

    # Test basic request
    response = client.get(url=url, params=params)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)

    # If we expect specific term, validate it
    if find_term_param.item:
        assert len(json_result) > 0
        for term in json_result:
            assert isinstance(term, dict)
            assert 'id' in term
            assert 'type' in term

        # Test with selected_term_fields
        params_with_select = params.copy()
        params_with_select['selected_term_fields'] = ['drs_name', 'nothing']

        response = client.get(url=url, params=params_with_select)
        assert response.status_code == 200

        json_result = response.json()
        for term in json_result:
            # With new behavior: only 'id' + selected fields that exist
            assert 'id' in term
            # 'nothing' should not be included (invalid field)
            assert 'nothing' not in term
            # 'type' and 'description' are NOT included when selected_term_fields is used


def test_find_terms_in_collection(client, find_term_param) -> None:
    """Test /search/terms/projects with collection_id filter."""
    url = '/terms/projects'
    project_id = find_term_param.item.project_id if find_term_param.item else DEFAULT_PROJECT
    collection_id = find_term_param.item.collection_id if find_term_param.item else DEFAULT_COLLECTION
    params = {'expression': find_term_param.expression,
              'project_id': project_id,
              'collection_id': collection_id}

    # Test basic request
    response = client.get(url=url, params=params)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)

    # If we expect specific term, validate it
    if find_term_param.item:
        assert len(json_result) > 0
        for term in json_result:
            assert isinstance(term, dict)
            assert 'id' in term
            assert 'type' in term

        # Test with selected_term_fields
        params_with_select = params.copy()
        params_with_select['selected_term_fields'] = ['drs_name', 'nothing']

        response = client.get(url=url, params=params_with_select)
        assert response.status_code == 200

        json_result = response.json()
        for term in json_result:
            # With new behavior: only 'id' + selected fields that exist
            assert 'id' in term
            # 'nothing' should not be included (invalid field)
            assert 'nothing' not in term
            # 'type' and 'description' are NOT included when selected_term_fields is used
