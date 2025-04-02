from esgvoc.api.data_descriptors import DATA_DESCRIPTOR_CLASS_MAPPING
from esgvoc.api.data_descriptors.data_descriptor import DataDescriptor
from esgvoc.api.project_specs import DrsType, ProjectSpecs
from esgvoc.api.search import Item, ItemKind, MatchingTerm
from fastapi.testclient import TestClient

from tests.api_inputs import check_id

_SELECT = {'selected_term_fields': ['drs_name', 'nothing']}


def instantiate(obj: list| dict | str) -> str | DataDescriptor | tuple | list | ProjectSpecs | \
                                          Item | MatchingTerm | None:
    result:str | DataDescriptor | tuple | list | ProjectSpecs | Item | MatchingTerm | None = None
    match obj:
        case str():
            result = obj
        case list():
            result = list()
            for item in obj:
                inst = instantiate(item)
                if inst:
                    result.append(inst)
            if not result:
                result = None
            elif len(result) == 1:
                result = result[0]
        case dict():
            if 'type' in obj:
                cls = DATA_DESCRIPTOR_CLASS_MAPPING[obj['type']]
                result = cls(**obj)
            elif 'drs_specs' in obj:
                result = ProjectSpecs(**obj)
            elif 'kind' in obj:
                result = Item(**obj)
            elif 'collection_id' in obj:
                result = MatchingTerm(**obj)
        case _:
            pass
    return result


def _test_get(client: TestClient, url: str, params: dict | None,
              id: str | None, select: bool,
              kind: ItemKind | None = None, parent_id: str | None = None) -> None:
    result = client.get(url=url, params=params)
    result.raise_for_status()
    json_result = result.json()
    assert json_result is not None
    if id:
        inst = instantiate(json_result)
        check_id(inst, id, kind, parent_id)
    if select:
        if params:
            params.update(_SELECT)
        else:
            params = _SELECT
        result = client.get(url=url, params=params)
        json_result = result.json()
        if isinstance(json_result, list):
            item = json_result[-1]
            if isinstance(item, list):
                assert len(item[-1]) == 4  # Cross case.
            else:
                assert len(item) == 4
        else:
            assert len(json_result) == 4

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
