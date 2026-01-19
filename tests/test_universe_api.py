import pytest

from esgvoc_backend import universe
from tests.api_inputs import get_param  # noqa: F401
from tests.utils import client_factory

router = universe.router

@pytest.fixture(scope='module')
def client(request):
    return client_factory(request, router)


def test_get_terms_in_universe(client) -> None:
    """Test GET /universe/terms returns all universe terms."""
    url = '/terms'

    # Test basic request
    response = client.get(url=url)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)
    assert len(json_result) > 0

    # Each item should be a term dict
    for term in json_result:
        assert isinstance(term, dict)
        assert 'id' in term
        assert 'type' in term
        assert 'description' in term

    # Test with selected_term_fields
    response = client.get(url=url, params={'selected_term_fields': ['drs_name', 'nothing']})
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)
    for term in json_result:
        # With new behavior: only 'id' + selected fields that exist
        assert 'id' in term
        # 'nothing' should not be included (invalid field)
        assert 'nothing' not in term
        # 'type' and 'description' are NOT included when selected_term_fields is used
        # 'drs_name' may or may not be present depending on term type


def test_get_term_in_universe(client, get_param) -> None:
    """Test GET /universe/terms/{term_id} returns specific term."""
    url = f'/terms/{get_param.term_id}'

    # Test basic request
    response = client.get(url=url)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, dict)
    assert json_result['id'] == get_param.term_id
    assert 'type' in json_result
    assert 'description' in json_result

    # Test with selected_term_fields
    response = client.get(url=url, params={'selected_term_fields': ['drs_name', 'nothing']})
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, dict)
    # With new behavior: only 'id' + selected fields that exist
    assert json_result['id'] == get_param.term_id
    # 'nothing' should not be included (invalid field)
    assert 'nothing' not in json_result
    # 'type' and 'description' are NOT included when selected_term_fields is used
    # 'drs_name' may or may not be present depending on term type


def test_get_data_descriptors(client, get_param):
    """Test GET /universe/data_descriptors returns all data descriptors."""
    url = '/data_descriptors'
    response = client.get(url=url)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)
    assert len(json_result) > 0

    # Check that requested data descriptor is in the list
    assert get_param.data_descriptor_id in json_result


def test_get_data_descriptor(client, get_param):
    """Test GET /universe/data_descriptors/{data_descriptor_id}."""
    url = f'/data_descriptors/{get_param.data_descriptor_id}'
    response = client.get(url=url)
    assert response.status_code == 200

    json_result = response.json()
    # Returns [data_descriptor_id, context_dict]
    assert isinstance(json_result, list)
    assert len(json_result) == 2
    data_descriptor_id, context = json_result
    assert data_descriptor_id == get_param.data_descriptor_id
    assert isinstance(context, dict)


def test_get_terms_in_data_descriptor(client, get_param) -> None:
    """Test GET /universe/data_descriptors/{data_descriptor_id}/terms."""
    url = f'/data_descriptors/{get_param.data_descriptor_id}/terms'

    # Test basic request
    response = client.get(url=url)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)
    assert len(json_result) > 0

    # Each item should be a term dict
    for term in json_result:
        assert isinstance(term, dict)
        assert 'id' in term
        assert 'type' in term
        assert 'description' in term

    # Check that requested term is in the list
    term_ids = [term['id'] for term in json_result]
    assert get_param.term_id in term_ids

    # Test with selected_term_fields
    response = client.get(url=url, params={'selected_term_fields': ['drs_name', 'nothing']})
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)
    for term in json_result:
        # With new behavior: only 'id' + selected fields that exist
        assert 'id' in term
        # 'nothing' should not be included (invalid field)
        assert 'nothing' not in term
        # 'type' and 'description' are NOT included when selected_term_fields is used
        # 'drs_name' may or may not be present depending on term type


def test_get_term_in_data_descriptor(client, get_param) -> None:
    """Test GET /universe/data_descriptors/{data_descriptor_id}/terms/{term_id}."""
    url = f'/data_descriptors/{get_param.data_descriptor_id}/terms/{get_param.term_id}'

    # Test basic request
    response = client.get(url=url)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, dict)
    assert json_result['id'] == get_param.term_id
    assert 'type' in json_result
    assert 'description' in json_result

    # Test with selected_term_fields
    response = client.get(url=url, params={'selected_term_fields': ['drs_name', 'nothing']})
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, dict)
    # With new behavior: only 'id' + selected fields that exist
    assert json_result['id'] == get_param.term_id
    # 'nothing' should not be included (invalid field)
    assert 'nothing' not in json_result
    # 'type' and 'description' are NOT included when selected_term_fields is used
    # 'drs_name' may or may not be present depending on term type


def test_get_suggested_terms_in_universe(client) -> None:
    """Test GET /universe/suggested/terms returns suggested terms."""
    url = '/suggested/terms'
    response = client.get(url=url)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)
    assert len(json_result) > 300
