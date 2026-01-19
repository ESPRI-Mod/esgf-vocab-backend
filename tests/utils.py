from typing import Any

import httpx
from esgvoc.api.data_descriptors import DATA_DESCRIPTOR_CLASS_MAPPING
from esgvoc.api.data_descriptors.data_descriptor import (
    DataDescriptor,
    PatternTermDataDescriptor,
    PlainTermDataDescriptor,
)
from esgvoc.api.project_specs import DrsType, ProjectSpecs
from esgvoc.api.search import Item, ItemKind, MatchingTerm
from fastapi.testclient import TestClient

from esgvoc_backend.constants import API_PREFIX, URI_PREFIX
from tests.api_inputs import check_id

_LOCALHOST = 'localhost:9999'
_SELECT = {'selected_term_fields': ['drs_name', 'nothing']}


def instantiate_from_json(json_obj: list| dict | str) -> str | DataDescriptor | tuple | list | \
                                                         ProjectSpecs | Item | MatchingTerm | None:
    result:str | DataDescriptor | tuple | list | ProjectSpecs | Item | MatchingTerm | None = None
    match json_obj:
        case str():
            result = json_obj
        case list():
            result = list()
            for item in json_obj:
                inst = instantiate_from_json(item)
                if inst:
                    result.append(inst)
            if not result:
                result = None
            elif len(result) == 1:
                result = result[0]
        case dict():
            if 'type' in json_obj:
                cls = DATA_DESCRIPTOR_CLASS_MAPPING[json_obj['type']]
                result = cls(**json_obj)
            elif 'drs_specs' in json_obj:
                result = ProjectSpecs(**json_obj)
            elif 'kind' in json_obj:
                result = Item(**json_obj)
            elif 'collection_id' in json_obj:
                result = MatchingTerm(**json_obj)
        case _:
            pass
    return result


def _test_get(client: httpx.Client, url: str, params: dict | None,
              id: str | None, select: bool,
              kind: ItemKind | None = None, parent_id: str | None = None) -> Any:
    result = client.get(url=url, params=params)
    result.raise_for_status()
    json_result = result.json()

    # First request: verify the term is present and get its type from JSON
    term_type = None
    if id:
        assert json_result is not None
        # Extract term type from JSON response (no instantiation)
        if isinstance(json_result, dict) and 'type' in json_result:
            term_type = json_result['type']
        elif isinstance(json_result, list):
            for item in json_result:
                if isinstance(item, dict) and 'type' in item:
                    term_type = item['type']
                    break
                elif isinstance(item, (tuple, list)) and len(item) > 0:
                    last_item = item[-1]
                    if isinstance(last_item, dict) and 'type' in last_item:
                        term_type = last_item['type']
                        break

    # Second request with selected_term_fields if needed
    if select:
        if params:
            params.update(_SELECT)
        else:
            params = _SELECT
        result = client.get(url=url, params=params)
        json_result = result.json()
        assert json_result

        # Determine if it's a PlainTerm based on the type
        # PlainTerms have drs_name, PatternTerms (like variant_label, time_range, member_id) don't
        plain_term_types = ['institution', 'source', 'variable', 'table', 'experiment', 'organisation', 'activity', 'grid']
        pattern_term_types = ['variant_label', 'time_range', 'member_id']

        is_plain_term = term_type in plain_term_types
        expected_field_count = 2 if is_plain_term else 1  # PlainTerm: id+drs_name, PatternTerm: id only

        if isinstance(json_result, list):
            item = json_result[-1]
            if isinstance(item, list):
                # Cross case: tuple contains (project_id, collection_id, term_dict)
                term_dict = item[-1]
                print(f"DEBUG: Cross case - item[-1] = {term_dict}, len = {len(term_dict)}, type = {term_type}, is_plain_term = {is_plain_term}")
                assert 'id' in term_dict  # id is always present
                assert 'nothing' not in term_dict  # invalid field should not be included
                assert len(term_dict) == expected_field_count
                if is_plain_term:
                    assert 'drs_name' in term_dict
            else:
                print(f"DEBUG: Single item case - item = {item}, type = {type(item)}, len = {len(item) if hasattr(item, '__len__') else 'N/A'}, term_type = {term_type}, is_plain_term = {is_plain_term}")
                assert 'id' in item
                assert 'nothing' not in item
                assert len(item) == expected_field_count
                if is_plain_term:
                    assert 'drs_name' in item
        else:
            assert 'id' in json_result
            assert 'nothing' not in json_result
            assert len(json_result) == expected_field_count
            if is_plain_term:
                assert 'drs_name' in json_result
    return json_result


def convert_drs_type(drs_type: DrsType) -> str:
    match drs_type:
        case DrsType.DIRECTORY:
            result = 'directory'
        case DrsType.FILE_NAME:
            result = 'filename'
        case DrsType.DATASET_ID:
            result = 'datasetid'
        case _:
            raise TypeError(f"unsupported drs type '{drs_type}'")
    return result


def client_factory(request, router, is_api: bool = True) -> httpx.Client:
    if request.param:
        if is_api:
            return httpx.Client(base_url=f'{request.param}{API_PREFIX}{router.prefix}')
        else:
            return httpx.Client(base_url=f'{request.param}{URI_PREFIX}{router.prefix}')
    else:
        return TestClient(router, base_url=f'http://{_LOCALHOST}{router.prefix}', backend='asyncio')
