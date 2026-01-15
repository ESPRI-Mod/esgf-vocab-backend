import pytest

from esgvoc_backend import projects
from tests.api_inputs import get_param  # noqa: F401
from tests.utils import client_factory

router = projects.router


@pytest.fixture(scope="module")
def client(request):
    return client_factory(request, router)


def test_get_projects(client, get_param) -> None:
    """Test GET /projects/ returns list of projects."""
    url = "/"
    response = client.get(url=url)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)
    assert len(json_result) > 0

    # Check that requested project is in the list
    assert get_param.project_id in json_result


def test_get_project(client, get_param) -> None:
    """Test GET /projects/{project_id} returns project details."""
    url = f"/{get_param.project_id}"
    response = client.get(url=url)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, dict)
    assert "project_id" in json_result
    assert json_result["project_id"] == get_param.project_id


def test_get_all_terms_in_project(client, get_param) -> None:
    """Test GET /projects/{project_id}/terms returns all terms."""
    url = f"/{get_param.project_id}/terms"

    # Test basic request
    response = client.get(url=url)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)
    assert len(json_result) > 0

    # Each item should be a term dict
    for term in json_result:
        assert isinstance(term, dict)
        assert "id" in term
        assert "type" in term
        assert "description" in term

    # Test with selected_term_fields
    response = client.get(url=url, params={"selected_term_fields": ["drs_name", "nothing"]})
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)
    for term in json_result:
        # With new behavior: only 'id' + selected fields that exist
        assert "id" in term
        # 'nothing' should not be included (invalid field)
        assert "nothing" not in term
        # 'type' and 'description' are NOT included when selected_term_fields is used


def test_get_collections_in_project(client, get_param) -> None:
    """Test GET /projects/{project_id}/collections returns all collections."""
    url = f"/{get_param.project_id}/collections"
    response = client.get(url=url)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)
    assert len(json_result) > 0

    # Check that requested collection is in the list
    assert get_param.collection_id in json_result


def test_get_all_terms_in_collection(client, get_param) -> None:
    """Test GET /projects/{project_id}/collections/{collection_id}/terms returns terms."""
    url = f"/{get_param.project_id}/collections/{get_param.collection_id}/terms"

    # Test basic request
    response = client.get(url=url)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)
    assert len(json_result) > 0

    # Each item should be a term dict
    for term in json_result:
        assert isinstance(term, dict)
        assert "id" in term
        assert "type" in term
        assert "description" in term

    # Check that requested term is in the list
    term_ids = [term["id"] for term in json_result]
    assert get_param.term_id in term_ids

    # Test with selected_term_fields
    response = client.get(url=url, params={"selected_term_fields": ["drs_name", "nothing"]})
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, list)
    for term in json_result:
        # With new behavior: only 'id' + selected fields that exist
        assert "id" in term
        # 'nothing' should not be included (invalid field)
        assert "nothing" not in term
        # 'type' and 'description' are NOT included when selected_term_fields is used


def test_get_term_in_project(client, get_param) -> None:
    """Test GET /projects/{project_id}/terms/{term_id} returns specific term."""
    url = f"/{get_param.project_id}/terms/{get_param.term_id}"

    # Test basic request
    response = client.get(url=url)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, dict)
    assert json_result["id"] == get_param.term_id
    assert "type" in json_result
    assert "description" in json_result

    # Test with selected_term_fields
    response = client.get(url=url, params={"selected_term_fields": ["drs_name", "nothing"]})
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, dict)
    # With new behavior: only 'id' + selected fields that exist
    assert json_result["id"] == get_param.term_id
    # 'nothing' should not be included (invalid field)
    assert "nothing" not in json_result
    # 'type' and 'description' are NOT included when selected_term_fields is used


def test_get_term_in_collection(client, get_param) -> None:
    """Test GET /projects/{project_id}/collections/{collection_id}/terms/{term_id}."""
    url = f"/{get_param.project_id}/collections/{get_param.collection_id}/terms/{get_param.term_id}"

    # Test basic request
    response = client.get(url=url)
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, dict)
    assert json_result["id"] == get_param.term_id
    assert "type" in json_result
    assert "description" in json_result

    # Test with selected_term_fields
    response = client.get(url=url, params={"selected_term_fields": ["drs_name", "nothing"]})
    assert response.status_code == 200

    json_result = response.json()
    assert isinstance(json_result, dict)
    # With new behavior: only 'id' + selected fields that exist
    assert json_result["id"] == get_param.term_id
    # 'nothing' should not be included (invalid field)
    assert "nothing" not in json_result
    # 'type' and 'description' are NOT included when selected_term_fields is used


def test_get_collection_in_project(client, get_param) -> None:
    """Test GET /projects/{project_id}/collections/{collection_id}."""
    url = f"/{get_param.project_id}/collections/{get_param.collection_id}"
    response = client.get(url=url)
    assert response.status_code == 200

    json_result = response.json()
    # Returns [collection_id, context_dict]
    assert isinstance(json_result, list)
    assert len(json_result) == 2
    collection_id, context = json_result
    assert collection_id == get_param.collection_id
    assert isinstance(context, dict)
