from collections.abc import Callable
from typing import Annotated, Any

import esgvoc.api.projects as projects
import esgvoc.api.universe as universe
from esgvoc.api.data_descriptors import DATA_DESCRIPTOR_CLASS_MAPPING
from esgvoc.api.data_descriptors.data_descriptor import DataDescriptor
from fastapi import APIRouter, Header, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse

router = APIRouter()

_UNIVERSE_CACHE:dict[str, dict[str, tuple[str, dict]]] = dict()
_PROJECTS_CACHE:dict[str, dict[str, dict[str, tuple[str, dict]]]] = dict()

def init_universe_cache() -> None:
    data_descriptors = universe.get_all_data_descriptors_in_universe()
    for data_descriptor in data_descriptors:
        _UNIVERSE_CACHE[data_descriptor] = dict()
        for term in universe.get_all_terms_in_data_descriptor(data_descriptor):
            _UNIVERSE_CACHE[data_descriptor][term.id] = jsonable_encoder(term), from_json_to_html(term)


def init_projects_cache() -> None:
    prjs = projects.get_all_projects()
    for project in prjs:
        _PROJECTS_CACHE[project] = dict()
        collections = projects.get_all_collections_in_project(project)
        for collection in collections:
            _PROJECTS_CACHE[project][collection] = dict()
            for term in projects.get_all_terms_in_collection(project, collection):
                _PROJECTS_CACHE[project][collection][term.id] = jsonable_encoder(term), from_json_to_html(term)


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


def format_term(term: tuple[str, dict], accept_type: str | None) -> JSONResponse | HTMLResponse:
    if accept_type is not None and "application/json" in accept_type:
        return JSONResponse(content=term[0])
    else:
        return HTMLResponse(term[1])


def create_universe_term_end_point(data_descriptor_id: str) -> Callable:
    def _end_point(term_id: str, accept: Annotated[str | None, Header()]):
        if term_id in _UNIVERSE_CACHE[data_descriptor_id]:
            return format_term(_UNIVERSE_CACHE[data_descriptor_id][term_id], accept)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="term not found")

    return _end_point


def create_universe_term_routes():
    for data_descriptor_id, _ in _UNIVERSE_CACHE.items():
        router.add_api_route(
            path=f"/universe/{data_descriptor_id}/{{term_id}}",
            endpoint=create_universe_term_end_point(data_descriptor_id),
            response_model=DATA_DESCRIPTOR_CLASS_MAPPING[data_descriptor_id],
            methods=["GET"],
        )


def create_project_term_end_point(project_id: str, collection_id: str) -> Callable:
    def _end_point(term_id: str, accept: Annotated[str | None, Header()]):
        if term_id in _PROJECTS_CACHE[project_id][collection_id]:
            return format_term(_PROJECTS_CACHE[project_id][collection_id][term_id], accept)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="term not found")

    return _end_point


def create_project_term_routes():
    for project_id, collection_contains in _PROJECTS_CACHE.items():
        for collection_id, _ in collection_contains.items():
            router.add_api_route(
                f"/{project_id}/{collection_id}/{{term_id}}",
                endpoint=create_project_term_end_point(project_id, collection_id),
                methods=["GET"],
            )


######################## MAIN #######################
init_universe_cache()
init_projects_cache()
create_universe_term_routes()
create_project_term_routes()
