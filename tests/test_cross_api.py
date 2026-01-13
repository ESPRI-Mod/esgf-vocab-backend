import pytest

from esgvoc_backend import cross
from tests.api_inputs import get_param  # noqa: F401
from tests.utils import _test_get, client_factory

router = cross.router


@pytest.fixture(scope="module")
def client(request):
    return client_factory(request, router)


def test_cross_term_in_all_projects(client, get_param) -> None:
    url = "/terms"
    if get_param.data_descriptor_id == "institution":
        dd_id = "organisation"
    else:
        dd_id = get_param.data_descriptor_id
    params = {"data_descriptor_id": dd_id, "universe_term_id": get_param.term_id}
    select = True
    _test_get(client, url, params, get_param.term_id, select)


def test_cross_term_in_project(client, get_param) -> None:
    url = "/terms"
    if get_param.data_descriptor_id == "institution":
        dd_id = "organisation"
    else:
        dd_id = get_param.data_descriptor_id
    params = {"project_id": get_param.project_id, "data_descriptor_id": dd_id, "universe_term_id": get_param.term_id}
    select = True
    _test_get(client, url, params, get_param.term_id, select)


def test_cross_collection_in_all_projects(client, get_param) -> None:
    url = "/collections"
    if get_param.data_descriptor_id == "institution":
        dd_id = "organisation"
    else:
        dd_id = get_param.data_descriptor_id
    params = {"data_descriptor_id": dd_id}
    select = False
    _test_get(client, url, params, get_param.collection_id, select)


def test_cross_collection_in_project(client, get_param) -> None:
    url = "/collections"
    if get_param.data_descriptor_id == "institution":
        dd_id = "organisation"
    else:
        dd_id = get_param.data_descriptor_id
    params = {"data_descriptor_id": dd_id, "project_id": get_param.project_id}
    select = False
    _test_get(client, url, params, get_param.collection_id, select)
