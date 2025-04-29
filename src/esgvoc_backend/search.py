from typing import Annotated

from esgvoc.api import projects, universe
from esgvoc.api.data_descriptors.data_descriptor import DataDescriptor
from esgvoc.api.search import Item
from fastapi import APIRouter, Query
from pydantic import SerializeAsAny

from esgvoc_backend.constants import PROJECTS_PAGE_PREFIX, UNIVERSE_PAGE_PREFIX
from esgvoc_backend.utils import generate_route_desc

router = APIRouter(prefix="/search")


@router.get("/items/universe",
            summary="Find items of the universe",
            description=generate_route_desc(f'{UNIVERSE_PAGE_PREFIX}.find_items_in_universe'))
async def find_items_in_universe(
    expression: Annotated[str, Query(description="keywords and boolean operators")],
    only_id: Annotated[bool, Query(description="search in id otherwise all specifications")] = False,
    limit: Annotated[int | None, Query(description="limit the number of returned items found")] = None,
    offset: Annotated[int | None, Query(description="skips offset number of items found")] = None) \
                                                            -> list[Item]:
    result = universe.find_items_in_universe(expression=expression, only_id=only_id,
                                             limit=limit, offset=offset)
    return result


@router.get("/items/projects",
            summary="Find items in a project",
            description=generate_route_desc(f'{UNIVERSE_PAGE_PREFIX}.find_items_in_project'))
async def find_items_in_project(
    expression: Annotated[str, Query(description="keywords and boolean operators")],
    project_id: Annotated[str, Query(description="an id of a project")],
    only_id: Annotated[bool, Query(description="search in id otherwise all specifications")] = False,
    limit: Annotated[int | None, Query(description="limit the number of returned items found")] = None,
    offset: Annotated[int | None, Query(description="skips offset number of items found")] = None) \
                                                            -> list[Item]:
    result = projects.find_items_in_project(expression=expression, project_id=project_id,
                                            only_id=only_id, limit=limit, offset=offset)
    return result


@router.get("/terms/universe",
            summary="Find terms in the universe and a data descriptor",
            description=generate_route_desc(f'{UNIVERSE_PAGE_PREFIX}.find_terms_in_universe',
                                            f'{UNIVERSE_PAGE_PREFIX}.find_terms_in_data_descriptor'))
async def find_terms_in_universe_data_descriptor(
    expression: Annotated[str, Query(description="keywords and boolean operators")],
    data_descriptor_id: Annotated[str | None, Query(description="An id of a data descriptor")] = None,
    only_id: Annotated[bool, Query(description="search in id otherwise all specifications")] = False,
    limit: Annotated[int | None, Query(description="limit the number of returned items found")] = None,
    offset: Annotated[int | None, Query(description="skips offset number of items found")] = None,
    selected_term_fields: Annotated[list[str] | None,
                                    Query(description="list of selected term fields, empty or null")] = None) \
                                                            -> list[SerializeAsAny[DataDescriptor]]:
    if data_descriptor_id:
        result = universe.find_terms_in_data_descriptor(expression=expression,
                                                        data_descriptor_id=data_descriptor_id,
                                                        only_id=only_id, limit=limit, offset=offset,
                                                        selected_term_fields=selected_term_fields)
    else:
        result = universe.find_terms_in_universe(expression=expression, only_id=only_id,
                                                 limit=limit, offset=offset,
                                                 selected_term_fields=selected_term_fields)
    return result


@router.get("/terms/projects",
            summary="Find terms in a project and a collection",
            description=generate_route_desc(f'{PROJECTS_PAGE_PREFIX}.find_terms_in_project',
                                            f'{PROJECTS_PAGE_PREFIX}.find_terms_in_collection'))
async def find_terms_in_project_collection(
    expression: Annotated[str, Query(description="keywords and boolean operators")],
    project_id: Annotated[str, Query(description="an id of a project")],
    collection_id: Annotated[str | None, Query(description="an id of a collection")] = None,
    only_id: Annotated[bool, Query(description="search in id otherwise all specifications")] = False,
    limit: Annotated[int | None, Query(description="limit the number of returned items found")] = None,
    offset: Annotated[int | None, Query(description="skips offset number of items found")] = None,
    selected_term_fields: Annotated[list[str] | None,
                                    Query(description="list of selected term fields, empty or null")] = None) \
                                                            -> list[SerializeAsAny[DataDescriptor]]:
    if collection_id:
        result = projects.find_terms_in_collection(expression=expression, project_id=project_id,
                                                   collection_id=collection_id, only_id=only_id,
                                                   limit=limit, offset=offset,
                                                   selected_term_fields=selected_term_fields)
    else:
        result = projects.find_terms_in_project(expression=expression, project_id=project_id,
                                                only_id=only_id, limit=limit, offset=offset,
                                                selected_term_fields=selected_term_fields)
    return result


@router.get("/data_descriptors",
            summary="Find data descriptors in the universe",
            description=generate_route_desc(f'{UNIVERSE_PAGE_PREFIX}.find_data_descriptors_in_universe'))
async def find_data_descriptors_in_universe(
    expression: Annotated[str, Query(description="keywords and boolean operators")],
    only_id: Annotated[bool, Query(description="search in id otherwise all specifications")] = False,
    limit: Annotated[int | None, Query(description="limit the number of returned items found")] = None,
    offset: Annotated[int | None, Query(description="skips offset number of items found")] = None) \
                                                                          -> list[tuple[str, dict]]:
    return universe.find_data_descriptors_in_universe(expression=expression, only_id=only_id,
                                                      limit=limit, offset=offset)


@router.get("/collections",
            summary="Find collections in a project",
            description=generate_route_desc(f'{PROJECTS_PAGE_PREFIX}.find_collections_in_project'))
async def find_collections_in_project(
    expression: Annotated[str, Query(description="keywords and boolean operators")],
    project_id: Annotated[str, Query(description='an id of a project')],
    only_id: Annotated[bool, Query(description="search in id otherwise all specifications")] = False,
    limit: Annotated[int | None, Query(description="limit the number of returned items found")] = None,
    offset: Annotated[int | None, Query(description="skips offset number of items found")] = None) \
                                                                          -> list[tuple[str, dict]]:
    return projects.find_collections_in_project(expression=expression,
                                                project_id=project_id,
                                                only_id=only_id, limit=limit, offset=offset)
