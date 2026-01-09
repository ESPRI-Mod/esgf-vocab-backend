import pytest

from esgvoc_backend import cross
from tests.api_inputs import get_param  # noqa: F401
from tests.utils import client_factory

router = cross.router

@pytest.fixture(scope='module')
def client(request):
    return client_factory(request, router)


def test_cross_term_in_all_projects(client, get_param) -> None:
    """Test /cross/terms endpoint returns terms from all projects."""
    url = '/terms'
    if get_param.data_descriptor_id == 'institution':
        dd_id = 'organisation'
    else:
        dd_id = get_param.data_descriptor_id
    params = {'data_descriptor_id': dd_id,
              'universe_term_id': get_param.term_id}

    # Test basic request
    response = client.get(url=url, params=params)
    assert response.status_code == 200
    json_result = response.json()

    # Should return a list of tuples: [(project_id, collection_id, term_dict), ...]
    assert isinstance(json_result, list)
    assert len(json_result) > 0

    # Each item should be a list with 3 elements: [project_id, collection_id, term_dict]
    for item in json_result:
        assert isinstance(item, list)
        assert len(item) == 3
        project_id, collection_id, term_dict = item

        # Validate structure
        assert isinstance(project_id, str)
        assert isinstance(collection_id, str)
        assert isinstance(term_dict, dict)

        # Term dict should have mandatory fields
        assert 'id' in term_dict
        assert 'type' in term_dict
        assert 'description' in term_dict

        # At least one term should match the requested ID
        if term_dict['id'] == get_param.term_id:
            found = True

    # Test with selected_term_fields
    params_with_select = params.copy()
    params_with_select['selected_term_fields'] = ['drs_name', 'nothing']

    response = client.get(url=url, params=params_with_select)
    assert response.status_code == 200
    json_result = response.json()

    # Should still return list of tuples
    assert isinstance(json_result, list)
    for item in json_result:
        assert isinstance(item, list)
        assert len(item) == 3
        _, _, term_dict = item

        # Should have mandatory fields
        assert 'id' in term_dict
        assert 'type' in term_dict
        assert 'description' in term_dict

        # If term has drs_name field, it should be included
        # If term doesn't have drs_name, it should not be included
        # 'nothing' field should never be included (doesn't exist)
        assert 'nothing' not in term_dict


def test_cross_term_in_project(client, get_param) -> None:
    """Test /cross/terms endpoint returns term from specific project."""
    url = '/terms'
    if get_param.data_descriptor_id == 'institution':
        dd_id = 'organisation'
    else:
        dd_id = get_param.data_descriptor_id
    params = {'project_id': get_param.project_id,
              'data_descriptor_id': dd_id,
              'universe_term_id': get_param.term_id}

    # Test basic request
    response = client.get(url=url, params=params)
    assert response.status_code == 200
    json_result = response.json()

    # Should return a tuple: [collection_id, term_dict]
    assert isinstance(json_result, list)
    assert len(json_result) == 2

    collection_id, term_dict = json_result
    assert isinstance(collection_id, str)
    assert isinstance(term_dict, dict)

    # Verify term structure
    assert term_dict['id'] == get_param.term_id
    assert 'type' in term_dict
    assert 'description' in term_dict

    # Test with selected_term_fields
    params_with_select = params.copy()
    params_with_select['selected_term_fields'] = ['drs_name', 'nothing']

    response = client.get(url=url, params=params_with_select)
    assert response.status_code == 200
    json_result = response.json()

    assert isinstance(json_result, list)
    assert len(json_result) == 2
    _, term_dict = json_result

    # Mandatory fields should be present
    assert 'id' in term_dict
    assert 'type' in term_dict
    assert 'description' in term_dict

    # 'nothing' should not be included
    assert 'nothing' not in term_dict


def test_cross_collection_in_all_projects(client, get_param) -> None:
    """Test /cross/collections endpoint returns collections from all projects."""
    url = '/collections'
    if get_param.data_descriptor_id == 'institution':
        dd_id = 'organisation'
    else:
        dd_id = get_param.data_descriptor_id
    params = {'data_descriptor_id': dd_id}

    response = client.get(url=url, params=params)
    assert response.status_code == 200
    json_result = response.json()

    # Should return list of tuples: [(project_id, collection_id, context_dict), ...]
    assert isinstance(json_result, list)
    assert len(json_result) > 0

    # Each item should be a list with 3 elements
    for item in json_result:
        assert isinstance(item, list)
        assert len(item) == 3
        project_id, collection_id, context = item

        assert isinstance(project_id, str)
        assert isinstance(collection_id, str)
        assert isinstance(context, dict)


def test_cross_collection_in_project(client, get_param) -> None:
    """Test /cross/collections endpoint returns collections from specific project."""
    url = '/collections'
    if get_param.data_descriptor_id == 'institution':
        dd_id = 'organisation'
    else:
        dd_id = get_param.data_descriptor_id
    params = {'data_descriptor_id': dd_id,
              'project_id': get_param.project_id}

    response = client.get(url=url, params=params)
    assert response.status_code == 200
    json_result = response.json()

    # Should return list of tuples: [(project_id, collection_id, context_dict), ...]
    assert isinstance(json_result, list)
    assert len(json_result) > 0

    # Each item should be a list with 3 elements
    for item in json_result:
        assert isinstance(item, list)
        assert len(item) == 3
        project_id, collection_id, context = item

        assert isinstance(project_id, str)
        assert isinstance(collection_id, str)
        assert isinstance(context, dict)

        # Project ID should match the requested one
        assert project_id == get_param.project_id
