from typing import Annotated

import esgvoc.api.projects as projects
from esgvoc.api.data_descriptors.data_descriptor import DataDescriptor
from esgvoc.api.project_specs import ProjectSpecs
from fastapi import APIRouter, Path, Query
from pydantic import SerializeAsAny

from esgvoc_backend.naming import PROJECTS_PAGE_PREFIX
from esgvoc_backend.utils import check_result, generate_route_desc

router = APIRouter(prefix="/projects")


@router.get("/",
            summary="Get all project ids",
            description=generate_route_desc(f'{PROJECTS_PAGE_PREFIX}.get_all_projects'))
async def get_all_projects() -> list[str]:
    return projects.get_all_projects()


@router.get("/{project_id}",
            summary="Get a project specs",
            description=generate_route_desc(f'{PROJECTS_PAGE_PREFIX}.get_project'))
async def get_project(project_id: Annotated[str, Path(description="an id of a project")]) -> ProjectSpecs | None:
    result = projects.get_project(project_id=project_id)
    return check_result(result)


@router.get("/{project_id}/terms",
            summary="Get all terms of a given project",
            description=generate_route_desc(f'{PROJECTS_PAGE_PREFIX}.get_all_terms_in_project'))
async def get_all_terms_in_project(
    project_id: Annotated[str, Path(description='an id of a project')],
    selected_term_fields: Annotated[list[str] | None,
                                    Query(description="list of selected term fields, empty or null")] = None) \
                                                            -> list[SerializeAsAny[DataDescriptor]]:
    result = projects.get_all_terms_in_project(project_id=project_id,
                                               selected_term_fields=selected_term_fields)
    return check_result(result)


@router.get("/{project_id}/terms/{term_id}",
            summary="Get a term of a given project",
            description=generate_route_desc(f'{PROJECTS_PAGE_PREFIX}.get_term_in_project'))
async def get_term_in_project(
    project_id: Annotated[str, Path(description='an id of a project')],
    term_id: Annotated[str, Path(description='an id of a term')],
    selected_term_fields: Annotated[list[str] | None,
                                    Query(description="list of selected term fields, empty or null")] = None) \
                                                                  -> SerializeAsAny[DataDescriptor]:
    result = projects.get_term_in_project(project_id=project_id, term_id=term_id,
                                          selected_term_fields=selected_term_fields)
    return check_result(result)


@router.get("/{project_id}/collections",
            summary="Get all collection ids of a given project",
            description=generate_route_desc(f'{PROJECTS_PAGE_PREFIX}.get_all_collections_in_project'))
async def get_all_collections_in_project(project_id: Annotated[str,
                                         Path(description='an id of a project')]) -> list[str]:
    result = projects.get_all_collections_in_project(project_id=project_id)
    return check_result(result)


@router.get("/{project_id}/collections/{collection_id}",
            summary="Get a collection of a given project",
            description=generate_route_desc(f'{PROJECTS_PAGE_PREFIX}.get_collection_in_project'))
async def get_collection_in_project(
        project_id: Annotated[str, Path(description='an id of a project')],
        collection_id: Annotated[str, Path(description='an id of a collection')]) -> tuple[str, dict]:
    result = projects.get_collection_in_project(project_id=project_id, collection_id=collection_id)
    return check_result(result)


@router.get("/{project_id}/collections/{collection_id}/terms",
            summary="Get all terms of a given collection",
            description=generate_route_desc(f'{PROJECTS_PAGE_PREFIX}.get_all_terms_in_collection'))
async def get_all_terms_in_collection(
    project_id: Annotated[str, Path(description='an id of a project')],
    collection_id: Annotated[str, Path(description='an id of a collection')],
    selected_term_fields: Annotated[list[str] | None,
                                    Query(description="list of selected term fields, empty or null")] = None) \
                                                            -> list[SerializeAsAny[DataDescriptor]]:
    result = projects.get_all_terms_in_collection(project_id=project_id, collection_id=collection_id,
                                                  selected_term_fields=selected_term_fields)
    return check_result(result)


@router.get("/{project_id}/collections/{collection_id}/terms/{term_id}",
            summary="Get a term of a given collection",
            description=generate_route_desc(f'{PROJECTS_PAGE_PREFIX}.get_term_in_collection'))
async def get_term_in_collection(
    project_id: Annotated[str, Path(description='an id of a project')],
    collection_id: Annotated[str, Path(description='an id of a collection')],
    term_id: Annotated[str, Path(description='an id of a term')],
    selected_term_fields: Annotated[list[str] | None,
                                    Query(description="list of selected term fields, empty or null")] = None) \
                                                                  -> SerializeAsAny[DataDescriptor]:
    result = projects.get_term_in_collection(project_id=project_id, collection_id=collection_id,
                                             term_id=term_id, selected_term_fields=selected_term_fields)
    return check_result(result)
