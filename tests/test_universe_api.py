import pytest

from esgvoc_backend import universe
from tests.api_inputs import get_param  # noqa: F401
from tests.utils import _test_get, client_factory

router = universe.router

@pytest.fixture(scope='module')
def client(request):
    return client_factory(request, router)


def test_get_terms_in_universe(client) -> None:
    url = '/terms'
    params = None
    select = True
    _test_get(client, url, params, None, select)


def test_get_term_in_universe(client, get_param) -> None:
    url = f'/terms/{get_param.term_id}'
    params = None
    select = True
    _test_get(client, url, params, get_param.term_id, select)


def test_get_data_descriptors(client, get_param):
    url = '/data_descriptors'
    params = None
    select = False
    _test_get(client, url, params, get_param.data_descriptor_id, select)


def test_get_data_descriptor(client, get_param):
    url = f'/data_descriptors/{get_param.data_descriptor_id}'
    params = None
    select = False
    _test_get(client, url, params, get_param.data_descriptor_id, select)


def test_get_terms_in_data_descriptor(client, get_param) -> None:
    url = f'/data_descriptors/{get_param.data_descriptor_id}/terms'
    params = None
    select = True
    _test_get(client, url, params, get_param.term_id, select)


def test_get_term_in_data_descriptor(client, get_param) -> None:
    url = f'/data_descriptors/{get_param.data_descriptor_id}/terms/{get_param.term_id}'
    params = None
    select = True
    _test_get(client, url, params, get_param.term_id, select)


def test_get_suggested_terms_in_universe(client) -> None:
    url = '/suggested/terms'
    params = None
    select = False
    result = _test_get(client, url, params, None, select)
    assert len(result) > 300
