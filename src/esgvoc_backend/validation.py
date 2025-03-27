from typing import Annotated

from esgvoc.api import projects
from esgvoc.api.report import ValidationReport
from esgvoc.api.search import MatchingTerm
from fastapi import APIRouter, Query

from esgvoc_backend.naming import PROJECTS_PAGE_PREFIX, generate_route_desc

router = APIRouter(prefix="/validation")


@router.get("/terms",
            summary="Valid a term",
            description=generate_route_desc(f'{PROJECTS_PAGE_PREFIX}.valid_term_in_all_projects',
                                            f'{PROJECTS_PAGE_PREFIX}.valid_term_in_project',
                                            f'{PROJECTS_PAGE_PREFIX}.valid_term_in_collection',
                                            f'{PROJECTS_PAGE_PREFIX}.valid_term'))
async def valid_term(
    value: Annotated[str, Query(description='the value to be validated')],
    project_id: Annotated[str | None, Query(description='an id of a project')] = None,
    collection_id: Annotated[str | None, Query(description='an id of a collection')] = None,
    term_id: Annotated[str | None, Query(description='an id of a term')] = None) \
                                                           -> list[MatchingTerm] | ValidationReport:
    result: list[MatchingTerm] | ValidationReport
    if project_id:
        if collection_id:
            if term_id:
                result = projects.valid_term(value=value, project_id=project_id,
                                             collection_id=collection_id, term_id=term_id)
            else:
                result = projects.valid_term_in_collection(value=value, project_id=project_id,
                                                           collection_id=collection_id)
        else:
            result = projects.valid_term_in_project(value=value, project_id=project_id)
    else:
        result = projects.valid_term_in_all_projects(value)
    return result
