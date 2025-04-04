from typing import Any, Generator

import pytest
from fastapi import FastAPI

import esgvoc_backend.uris as uris
from tests.utils import client_factory

router = uris.router
_APP = FastAPI()
_APP.include_router(router)

@pytest.fixture(scope='module')
def client(request):
    return client_factory(request, router, False)


_SOME_URIS = [
    'cmip6plus/variable_id/bsi',
    'cmip6/activity_id/c4mip',
    'universe/institution/ipsl',
    'universe/grid/gn',
    'universe/variable/arag',
]


def _provide_uris() -> Generator:
    for expression in _SOME_URIS:
        yield expression


@pytest.fixture(params=_provide_uris())
def uri(request) -> dict[str, Any]:
    return request.param


def test_uris(client, uri) -> None:
    result = client.get(url=uri)
    result.raise_for_status()
