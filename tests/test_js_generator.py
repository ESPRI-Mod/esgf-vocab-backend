from typing import Generator

import pytest

from esgvoc_backend import jsg
from tests.utils import _test_get, client_factory

router = jsg.router

JSG_PROJECT_IDS = ["cmip6"]


@pytest.fixture(scope='module')
def client(request):
    return client_factory(request, router)


def _provide_get_jsg_project_ids() -> Generator:
    for param in JSG_PROJECT_IDS:
        yield param

@pytest.fixture(params=_provide_get_jsg_project_ids())
def jsg_project_id(request) -> str:
    return request.param


def test_js_generation(client, jsg_project_id) -> None:
    url = f'/{jsg_project_id}'
    json_result = _test_get(client=client, url=url, params=None, select=False, id=None)
    assert json_result
