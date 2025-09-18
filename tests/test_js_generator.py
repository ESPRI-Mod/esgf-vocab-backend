import pytest

from esgvoc_backend import jsg
from tests.api_inputs import project_id  # noqa: F401
from tests.utils import _test_get, client_factory

router = jsg.router


@pytest.fixture(scope='module')
def client(request):
    return client_factory(request, router)


def test_js_generation(client, project_id) -> None:
    url = f'/{project_id}'
    json_result = _test_get(client=client, url=url, params=None, select=False, id=None)
    assert json_result
