from typing import Annotated

from esgvoc.api import projects
from esgvoc.api.data_descriptors.data_descriptor import DataDescriptor
from fastapi import APIRouter, Query
from pydantic import SerializeAsAny

from esgvoc_backend.naming import PROJECTS_PAGE_PREFIX, generate_route_desc
from esgvoc_backend.utils import check_result

router = APIRouter(prefix="/cross")


@router.get("/terms",
            summary="Get the corresponding project terms",
            description=generate_route_desc(f'{PROJECTS_PAGE_PREFIX}.get_term_from_universe_term_id_in_project',
                                            f'{PROJECTS_PAGE_PREFIX}.get_term_from_universe_term_id_in_all_projects'))
async def cross_terms_in_projects(
    data_descriptor_id: Annotated[str, Query(description="an id of a data descriptor")],
    universe_term_id: Annotated[str, Query(description="an id of a universe term")],
    project_id: Annotated[str | None, Query(description="an id of project")] = None,
    selected_term_fields: Annotated[list[str] | None,
                                    Query(description="list of selected term fields, empty or null")] = None) \
            -> tuple[str, SerializeAsAny[DataDescriptor]] | list[tuple[str, str, SerializeAsAny[DataDescriptor]]]:
    result: tuple[str, DataDescriptor] | list[tuple[str, str, DataDescriptor]]
    if project_id:
        result = check_result(projects.get_term_from_universe_term_id_in_project(
                                                           project_id=project_id,
                                                           data_descriptor_id=data_descriptor_id,
                                                           universe_term_id=universe_term_id,
                                                           selected_term_fields=selected_term_fields))
    else:
        result = projects.get_term_from_universe_term_id_in_all_projects(data_descriptor_id=data_descriptor_id,
                                                                         universe_term_id=universe_term_id,
                                                                         selected_term_fields=selected_term_fields)
    return result


@router.get("/collections",
            summary="Get the corresponding collection",
            description=generate_route_desc(f'{PROJECTS_PAGE_PREFIX}.get_collection_from_data_descriptor_in_project',
                                            f'{PROJECTS_PAGE_PREFIX}.get_collection_from_data_descriptor_in_all_projects'))  # noqa
async def cross_collections_in_project(
    data_descriptor_id: Annotated[str, Query(description="an id of a data descriptor")],
    project_id: Annotated[str | None, Query(description="an id of project")] = None) \
                                                  -> tuple[str, dict] | list[tuple[str, str, dict]]:
    result: tuple[str, dict] | list[tuple[str, str, dict]]
    if project_id:
        tmp = projects.get_collection_from_data_descriptor_in_project(project_id=project_id,
                                                                      data_descriptor_id=data_descriptor_id)
        result = check_result(tmp)
    else:
        result = projects.get_collection_from_data_descriptor_in_all_projects(data_descriptor_id=data_descriptor_id)
    return result
