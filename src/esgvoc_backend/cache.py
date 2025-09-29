import logging
from typing import Any

import esgvoc.api.projects as projects
import esgvoc.api.universe as universe
from esgvoc.api.data_descriptors.data_descriptor import DataDescriptor
from esgvoc.apps.drs.generator import DrsGenerator
from esgvoc.apps.drs.validator import DrsValidator
from esgvoc.apps.jsg.json_schema_generator import generate_json_schema
from esgvoc.core.exceptions import EsgvocException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

_LOGGER = logging.getLogger(__name__)

PROJECT_IDS = projects.get_all_projects()


def init_drs_cache() -> tuple[dict[str, DrsValidator], dict[str, DrsGenerator]]:
    validators: dict[str, DrsValidator] = dict()
    generators: dict[str, DrsGenerator] = dict()
    for project_id in PROJECT_IDS:
        validators[project_id] = DrsValidator(project_id=project_id)
        generators[project_id] = DrsGenerator(project_id=project_id)
        _LOGGER.info(f'{project_id} DRS cache loaded')
    return validators, generators


VALIDATORS, GENERATORS = init_drs_cache()


def _to_str(value: list | dict | Any) -> str:
    result = ""
    if isinstance(value, list):
        match len(value):
            case 0:
                pass
            case 1:
                result = _to_str(value[0])
            case _:
                result = str(value)
    elif isinstance(value, dict):
        return str(value)
    else:
        result = str(value)
    return result


def _from_json_to_html(term: DataDescriptor) -> str:
    result = "<!DOCTYPE html>\n<html>\n<body>\n<ul>\n"
    for key, value in term.model_dump().items():
        result += f"<li>{key}: {_to_str(value)}</li>\n"
    result += "</ul>\n</body>\n</html>"
    return result


def _init_universe_cache() -> dict[str, dict[str, tuple[Any, str, DataDescriptor]]]:
    result: dict[str, dict[str, tuple[Any, str, DataDescriptor]]] = dict()
    data_descriptors = universe.get_all_data_descriptors_in_universe()
    for data_descriptor in data_descriptors:
        result[data_descriptor] = dict()
        for term in universe.get_all_terms_in_data_descriptor(data_descriptor):
            result[data_descriptor][term.id] = jsonable_encoder(term), _from_json_to_html(term), term
    _LOGGER.info('universe cache loaded')
    return result


UNIVERSE_CACHE: dict[str, dict[str, tuple[Any, str, DataDescriptor]]] = _init_universe_cache()


def _init_projects_cache() -> tuple[dict[str, str],
                                    dict[str, dict[str, dict[str, tuple[Any, str, DataDescriptor]]]]]:
    projects_cache: dict[str, dict[str, dict[str, tuple[Any, str, DataDescriptor]]]] = dict()
    collection_data_descriptor_mapping: dict[str, str] = dict()
    for project_id in PROJECT_IDS:
        projects_cache[project_id] = dict()
        with projects._get_project_connection(project_id).create_session() as session:  # type: ignore
            collections = projects._get_all_collections_in_project(session)
            for collection in collections:
                collection_data_descriptor_mapping[collection.id] = collection.data_descriptor_id
                projects_cache[project_id][collection.id] = dict()
                for term in projects._get_all_terms_in_collection(collection, None):
                    projects_cache[project_id][collection.id][term.id] = jsonable_encoder(term), \
                                                                         _from_json_to_html(term), \
                                                                         term
        _LOGGER.info(f'{project_id} cache loaded')
    return collection_data_descriptor_mapping, projects_cache


COLLECTION_DATA_DESCRIPTOR_MAPPING, PROJECTS_CACHE = _init_projects_cache()


class SuggestedTerm(BaseModel):
    type: str
    id: str


def _init_suggested_terms_cache() -> list[SuggestedTerm]:  # Execute after init_universe_cache!
    result: list[SuggestedTerm] = list()
    for data_descriptor_id in UNIVERSE_CACHE.keys():
        count = 0
        for term_id in UNIVERSE_CACHE[data_descriptor_id].keys():
            result.append(SuggestedTerm(type=data_descriptor_id, id=term_id))
            count += 1
            if count > 19:
                break
    _LOGGER.info('suggested terms cache loaded')
    return result


SUGGESTED_TERMS_OF_UNIVERSE: list[SuggestedTerm] = _init_suggested_terms_cache()


def _init_stac_json_schemas() -> dict[str, dict]:
    result: dict[str, dict] = dict()
    for project_id in PROJECT_IDS:
        try:
            result[project_id] = generate_json_schema(project_id)
            _LOGGER.info(f'{project_id} json schema cache loaded')
        except EsgvocException as e:
            msg = f'unable to generate json schema for project {project_id}, skip: {e}'
            _LOGGER.error(msg)
            continue
    return result


STAC_JSON_SCHEMAS: dict[str, dict] = _init_stac_json_schemas()
