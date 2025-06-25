import pytest

from esgvoc_backend import jsg
from tests.utils import _test_get, client_factory

router = jsg.router


@pytest.fixture(scope='module')
def client(request):
    return client_factory(request, router)


def test_cmip6_js_generation(client) -> None:
    project_id = 'cmip6'
    url = f'/{project_id}'
    json_result = _test_get(client=client, url=url, params=None, select=False, id=None)
    assert json_result
