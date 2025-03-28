from typing import Generator

import pytest
from fastapi.testclient import TestClient

_SELECT = {'selected_term_fields': ['drs_name', 'nothing']}
# TODO: refactor into data class.
_SOME_PROJECT_IDS = ['cmip6plus', 'cmip6']
_SOME_COLLECTION_IDS = ['institution_id', 'time_range', 'source_id']
_SOME_DATA_DESCRIPTOR_IDS = ['institution', 'time_range', 'source']
_SOME_TERM_IDS = ['ipsl', 'daily', 'miroc6']
_SOME_DD_TERM_IDS = [(_SOME_DATA_DESCRIPTOR_IDS[0], _SOME_TERM_IDS[0]),
                     (_SOME_DATA_DESCRIPTOR_IDS[1], _SOME_TERM_IDS[1]),
                     (_SOME_DATA_DESCRIPTOR_IDS[2], _SOME_TERM_IDS[2])]
_SOME_PROJ_DD_COL_TERM_IDS = [
    (_SOME_PROJECT_IDS[0], _SOME_DATA_DESCRIPTOR_IDS[0], _SOME_COLLECTION_IDS[0], _SOME_TERM_IDS[0]),
    (_SOME_PROJECT_IDS[0], _SOME_DATA_DESCRIPTOR_IDS[1], _SOME_COLLECTION_IDS[1], _SOME_TERM_IDS[1]),
    (_SOME_PROJECT_IDS[0], _SOME_DATA_DESCRIPTOR_IDS[2], _SOME_COLLECTION_IDS[2], _SOME_TERM_IDS[2]),
    (_SOME_PROJECT_IDS[1], _SOME_DATA_DESCRIPTOR_IDS[0], _SOME_COLLECTION_IDS[0], _SOME_TERM_IDS[0]),
    (_SOME_PROJECT_IDS[1], _SOME_DATA_DESCRIPTOR_IDS[1], _SOME_COLLECTION_IDS[1], _SOME_TERM_IDS[1]),
    (_SOME_PROJECT_IDS[1], _SOME_DATA_DESCRIPTOR_IDS[2], _SOME_COLLECTION_IDS[2], _SOME_TERM_IDS[2])]


def check_id(json_result: dict | list | tuple, id: str, min_items: int | None = None) -> None:
    match json_result:
        case list():
            if min_items:
                assert len(json_result) >= min_items
            found = False
            for r in json_result:
                try:
                    check_id(r, id, None)
                    found = True
                    break
                except Exception:  # noqa: S112
                    continue
            assert found
        case str():
            assert id == json_result
        case dict():
            if min_items:
                assert min_items == 1
            if 'id' in json_result:
                assert id == json_result['id']
            else:
                assert id == json_result['project_id']
        case _:
            raise RuntimeError(f'unsupported json result {type(json_result)}')


def _test_get(client: TestClient, url: str, params: dict | None,
              min_items: int, id: str | None, select: bool) -> None:
    result = client.get(url=url, params=params)
    result.raise_for_status()
    if min_items > 0:
        json_result = result.json()
        assert json_result is not None
        if id:
            check_id(json_result, id, min_items)
        if select:
            if params:
                params.update(_SELECT)
            else:
                params = _SELECT
            result = client.get(url=url, params=params)
            json_result = result.json()
            assert len(json_result) >= min_items
            if isinstance(json_result, list):
                item = json_result[-1]
                if isinstance(item, list):
                    assert len(item[-1]) == 4  # Cross case.
                else:
                    assert len(item) == 4
            else:
                assert len(json_result) == 4
    else:
        assert result.json() is None


def _provide_project_ids() -> Generator:
    for project_id in _SOME_PROJECT_IDS:
        yield project_id


@pytest.fixture(params=_provide_project_ids())
def project_id(request) -> str:
    return request.param


def _provide_collection_ids() -> Generator:
    for collection_id in _SOME_COLLECTION_IDS:
        yield collection_id


def _provide_data_descriptor_ids() -> Generator:
    for combo in _SOME_DATA_DESCRIPTOR_IDS:
        yield combo


@pytest.fixture(params=_provide_data_descriptor_ids())
def data_descriptor_id(request) -> str:
    return request.param


@pytest.fixture(params=_provide_collection_ids())
def collection_id(request) -> str:
    return request.param


def _provide_term_ids() -> Generator:
    for term_id in _SOME_TERM_IDS:
        yield term_id


@pytest.fixture(params=_provide_term_ids())
def term_id(request) -> str:
    return request.param


def _provide_proj_dd_col_ids() -> Generator:
    for combo in _SOME_PROJ_DD_COL_TERM_IDS:
        yield combo


@pytest.fixture(params=_provide_proj_dd_col_ids())
def proj_dd_col_term_id(request) -> tuple[str, str, str, str]:
    return request.param


def _provide_dd_term_ids() -> Generator:
    for combo in _SOME_DD_TERM_IDS:
        yield combo


@pytest.fixture(params=_provide_dd_term_ids())
def dd_term_ids(request) -> tuple[str, str]:
    return request.param
