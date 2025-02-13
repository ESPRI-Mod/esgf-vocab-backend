from typing import Annotated

import esgvoc.api.projects as projects
from esgvoc.api.data_descriptors.data_descriptor import DataDescriptor
from esgvoc.api.project_specs import ProjectSpecs
from esgvoc.api.projects import MatchingTerm
from esgvoc.api.report import ValidationReport
from esgvoc.api.search import SearchSettings
from fastapi import APIRouter, HTTPException, Path, Query, status

router = APIRouter(prefix="/projects")

"""
/projects                 => get_all_projects
/projects/find?project_id => find_project

/projects/terms                                  => get_all_terms_in_all_projects
/projects/terms/find?term_id                     => find_terms_in_all_projects
/projects/terms/valid?value                      => valid_term_in_all_projects
/projects/terms/cross?term_id&data_descriptor_id => find_terms_from_data_descriptor_in_all_projects

/projects/{project_id}/terms                                  => get_all_terms_in_project
/projects/{project_id}/terms/find?term_id                     => find_terms_in_project
/projects/{project_id}/terms/valid?value                      => valid_term_in_project
/projects/{project_id}/terms/cross?term_id&data_descriptor_id => find_terms_from_data_descriptor_in_project

/projects/{project_id}/collections                    => get_all_collections_in_project
/projects/{project_id}/collections/find?collection_id => find_collections_in_project

/projects/{project_id}/collections/{collection_id}/terms                     => get_all_terms_in_collection
/projects/{project_id}/collections/{collection_id}/terms/find?term_id        => find_terms_in_collection
/projects/{project_id}/collections/{collection_id}/terms/valid?value         => valid_term_in_collection
/projects/{project_id}/collections/{collection_id}/terms/valid?term_id&value => valid_term
"""


@router.get("/", summary="Get all project ids")
async def get_projects() -> list[str]:
    return projects.get_all_projects()


@router.get("/find", summary="Find projects")
async def find_project(
        project_id: Annotated[str, Query(description="The project to be found")])-> ProjectSpecs|None:
    return projects.find_project(project_id=project_id)


@router.get("/terms", summary="Get all terms of all projects")
async def get_all_terms_in_all_projects(
    selected_term_fields: \
            Annotated[list[str] | None, Query(description="Selected term fields or null")] = None) \
                                                                            -> list[DataDescriptor]:
    return projects.get_all_terms_in_all_projects(selected_term_fields=selected_term_fields)


@router.post("/terms/find", summary="Find terms in all projects")
async def find_terms_in_all_projects(
        term_id: Annotated[str, Query(description="The terms to be found")],
        settings: SearchSettings | None = None) -> list[DataDescriptor]:
    return projects.find_terms_in_all_projects(term_id=term_id, settings=settings)


@router.get("/terms/valid", summary="Valid term against all terms of in all projects")
async def valid_term_in_all_projects(
        value: Annotated[str, Query(description='The value to be validated')]) -> list[MatchingTerm]:
    return projects.valid_term_in_all_projects(value)


@router.post("/terms/cross", summary="Find terms according to a given data descriptor in all projects")
async def cross_terms_in_all_projects(
        data_descriptor_id: Annotated[str, Query(description="The given data descriptor")],
        term_id: Annotated[str, Query(description="The terms to be found")],
        settings: SearchSettings | None = None) -> list[tuple[list[tuple[DataDescriptor, str]], str]]:
    return projects.find_terms_from_data_descriptor_in_all_projects(
        data_descriptor_id=data_descriptor_id,
        term_id=term_id,
        settings=settings)


@router.get("/{project_id}/terms", summary="Get all terms of a given project")
async def get_all_terms_in_project(
        project_id: Annotated[str, Path(description='The given project')],
        selected_term_fields: \
            Annotated[list[str] | None, Query(description="Selected term fields or null")] = None) \
                                                                            -> list[DataDescriptor]:
    return projects.get_all_terms_in_project(project_id=project_id,
                                             selected_term_fields=selected_term_fields)


@router.post("/{project_id}/terms/find", summary="Find terms in a given project")
async def find_terms_in_project(
        project_id: Annotated[str, Path(description='The given project')],
        term_id: Annotated[str, Query(description="The terms to be found")],
        settings: SearchSettings | None = None) -> list[DataDescriptor]:
    return projects.find_terms_in_project(project_id=project_id, term_id=term_id,settings=settings)


@router.get("/{project_id}/terms/valid", summary="Valid term against all terms of a given project")
async def valid_term_in_project(
        project_id: Annotated[str, Path(description='The given project')],
        value: Annotated[str, Query(description='The value to be validated')]) -> list[MatchingTerm]:
    try:
        return projects.valid_term_in_project(value=value, project_id=project_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{project_id}/terms/cross", summary="Find terms according to a given data descriptor in a given project")
async def cross_terms_in_project(
        project_id: Annotated[str, Path(description='The given project')],
        data_descriptor_id: Annotated[str, Query(description="The given data descriptor")],
        term_id: Annotated[str, Query(description="The terms to be found")],
        settings: SearchSettings | None = None) -> list[tuple[DataDescriptor, str]]:
    return projects.find_terms_from_data_descriptor_in_project(project_id=project_id,
                                                               data_descriptor_id=data_descriptor_id,
                                                               term_id=term_id,
                                                               settings=settings)


@router.get("/{project_id}/collections", summary="Get all collection ids of a given project")
async def get_collections_in_project(
        project_id: Annotated[str, Path(description='The given project')]) -> list[str]:
    return projects.get_all_collections_in_project(project_id=project_id)


@router.post("/{project_id}/collections/find", summary="Find collections in a given project")
async def find_collections_in_project(
        project_id: Annotated[str, Path(description='The given project')],
        collection_id: Annotated[str, Query(description="The collections to be found")],
        settings: SearchSettings | None = None) -> list[dict]:
    return projects.find_collections_in_project(project_id=project_id, collection_id=collection_id,
                                                settings=settings)


@router.get("/{project_id}/collections/{collection_id}/terms",
            summary="Get all terms of a given collection")
async def get_terms_in_collection(
        project_id: Annotated[str, Path(description='The project of the collection')],
        collection_id: Annotated[str, Path(description='The given collection')],
        selected_term_fields: \
            Annotated[list[str] | None, Query(description="Selected term fields or null")] = None) \
                                                                            -> list[DataDescriptor]:
    return projects.get_all_terms_in_collection(project_id=project_id, collection_id=collection_id,
                                                selected_term_fields=selected_term_fields)


@router.post("/{project_id}/collections/{collection_id}/terms/find",
             summary="Find terms in a given collection")
async def find_terms_in_collection(
        project_id: Annotated[str, Path(description='The project of the collection')],
        collection_id: Annotated[str, Path(description='The given collection')],
        term_id: Annotated[str, Query(description="The terms to be found")],
        settings: SearchSettings | None = None) -> list[DataDescriptor]:
    return projects.find_terms_in_collection(project_id=project_id, collection_id=collection_id,
                                             term_id=term_id, settings=settings)


@router.get("/{project_id}/collections/{collection_id}/terms/valid",
            summary="Valid term against a specific term or all terms of a given collection")
async def valid_term_in_collection(
        project_id: Annotated[str, Path(description='The project of the collection')],
        collection_id: Annotated[str, Path(description='A given collection')],
        value: Annotated[str, Query(description='The value to be validated')],
        term_id: Annotated[str|None, Query(description='A specific term')] = None) \
                                                             -> list[MatchingTerm]|ValidationReport:
    try:
        if term_id:
            return projects.valid_term(value=value, project_id=project_id,
                                       collection_id=collection_id, term_id=term_id)
        else:
            return projects.valid_term_in_collection(value=value, project_id=project_id,
                                                     collection_id=collection_id)
    except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
