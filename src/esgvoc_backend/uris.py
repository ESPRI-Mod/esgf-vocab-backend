from collections.abc import Callable
from typing import Annotated, Any

from esgvoc.api.data_descriptors import DATA_DESCRIPTOR_CLASS_MAPPING
from esgvoc.api.data_descriptors.data_descriptor import DataDescriptor
from fastapi import APIRouter, Header, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse

from esgvoc_backend.cache import COLLECTION_DATA_DESCRIPTOR_MAPPING, PROJECTS_CACHE, UNIVERSE_CACHE

router = APIRouter()


def format_term(term: tuple[Any, str, DataDescriptor], accept_type: str | None) -> JSONResponse | HTMLResponse:
    if accept_type is not None and "application/json" in accept_type:
        return JSONResponse(content=term[0])
    else:
        return HTMLResponse(term[1])


def create_universe_term_end_point(data_descriptor_id: str) -> Callable:
    def _end_point(term_id: str, accept: Annotated[str | None, Header()] = None):
        if term_id in UNIVERSE_CACHE[data_descriptor_id]:
            return format_term(UNIVERSE_CACHE[data_descriptor_id][term_id], accept)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="term not found")

    return _end_point


def create_universe_term_routes():
    for data_descriptor_id, _ in UNIVERSE_CACHE.items():
        router.add_api_route(
            path=f"/universe/{data_descriptor_id}/{{term_id}}",
            endpoint=create_universe_term_end_point(data_descriptor_id),
            response_model=DATA_DESCRIPTOR_CLASS_MAPPING[data_descriptor_id],
            methods=["GET"],
        )


def create_project_term_end_point(project_id: str, collection_id: str) -> Callable:
    def _end_point(term_id: str, accept: Annotated[str | None, Header()] = None):
        if term_id in PROJECTS_CACHE[project_id][collection_id]:
            return format_term(PROJECTS_CACHE[project_id][collection_id][term_id], accept)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="term not found")

    return _end_point


def create_project_term_routes():
    for project_id, collection_contains in PROJECTS_CACHE.items():
        for collection_id, _ in collection_contains.items():
            data_descriptor_id = COLLECTION_DATA_DESCRIPTOR_MAPPING[collection_id]
            router.add_api_route(
                f"/{project_id}/{collection_id}/{{term_id}}",
                endpoint=create_project_term_end_point(project_id, collection_id),
                response_model=DATA_DESCRIPTOR_CLASS_MAPPING[data_descriptor_id],
                methods=["GET"],
            )


# MAIN
create_universe_term_routes()
create_project_term_routes()
