from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import esgvoc_backend.uris as uris

_BASE_URL = 'http://localhost:9999'
_APP = FastAPI()
_APP.include_router(uris.router)
_CLIENT = TestClient(_APP, base_url=_BASE_URL, backend='asyncio')

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
def uri(request) -> dict[str, any]:
    return request.param


def test_uris(uri) -> None:
    result = _CLIENT.get(url=uri)
    result.raise_for_status()
