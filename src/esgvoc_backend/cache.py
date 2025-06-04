from typing import Any

import esgvoc.api.projects as projects
import esgvoc.api.universe as universe
from esgvoc.api.data_descriptors.data_descriptor import DataDescriptor
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class SuggestedTerm(BaseModel):
    type: str
    id: str


SUGGESTED_TERMS_OF_UNIVERSE: list[SuggestedTerm] = list()
UNIVERSE_CACHE: dict[str, dict[str, tuple[Any, str, DataDescriptor]]] = dict()
PROJECTS_CACHE: dict[str, dict[str, dict[str, tuple[Any, str, DataDescriptor]]]] = dict()
COLLECTION_DATA_DESCRIPTOR_MAPPING: dict[str, str] = dict()


def to_str(value: list | dict | Any) -> str:
    result = ""
    if isinstance(value, list):
        match len(value):
            case 0:
                pass
            case 1:
                result = to_str(value[0])
            case _:
                result = str(value)
    elif isinstance(value, dict):
        return str(value)
    else:
        result = str(value)
    return result


def from_json_to_html(term: DataDescriptor) -> str:
    result = "<!DOCTYPE html>\n<html>\n<body>\n<ul>\n"
    for key, value in term.model_dump().items():
        result += f"<li>{key}: {to_str(value)}</li>\n"
    result += "</ul>\n</body>\n</html>"
    return result


def init_universe_cache() -> None:
    data_descriptors = universe.get_all_data_descriptors_in_universe()
    for data_descriptor in data_descriptors:
        UNIVERSE_CACHE[data_descriptor] = dict()
        for term in universe.get_all_terms_in_data_descriptor(data_descriptor):
            UNIVERSE_CACHE[data_descriptor][term.id] = jsonable_encoder(term), from_json_to_html(term), term


def init_projects_cache() -> None:
    project_ids = projects.get_all_projects()
    for project_id in project_ids:
        PROJECTS_CACHE[project_id] = dict()
        with projects._get_project_connection(project_id).create_session() as session:  # type: ignore
            collections = projects._get_all_collections_in_project(session)
            for collection in collections:
                COLLECTION_DATA_DESCRIPTOR_MAPPING[collection.id] = collection.data_descriptor_id
                PROJECTS_CACHE[project_id][collection.id] = dict()
                for term in projects._get_all_terms_in_collection(collection, None):
                    PROJECTS_CACHE[project_id][collection.id][term.id] = jsonable_encoder(term), \
                                                                         from_json_to_html(term), \
                                                                         term


def init_suggested_terms_cache() -> None:  # Execute after init_universe_cache!
    for data_descriptor_id in UNIVERSE_CACHE.keys():
        count = 0
        for term_id in UNIVERSE_CACHE[data_descriptor_id].keys():
            SUGGESTED_TERMS_OF_UNIVERSE.append(SuggestedTerm(type=data_descriptor_id,
                                                             id=term_id))
            count += 1
            if count > 19:
                break


init_universe_cache()
init_projects_cache()
init_suggested_terms_cache()
