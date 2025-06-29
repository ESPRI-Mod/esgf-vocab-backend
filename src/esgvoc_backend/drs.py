from typing import Annotated

from esgvoc.api.project_specs import DrsType
from esgvoc.apps.drs.report import DrsGenerationReport, DrsValidationReport
from fastapi import APIRouter, HTTPException, Path, Query, status

from esgvoc_backend.cache import GENERATORS, VALIDATORS
from esgvoc_backend.constants import DRS_GEN_PREFIX, DRS_VAL_PREFIX
from esgvoc_backend.utils import generate_route_desc

router = APIRouter(prefix="/apps/drs")


def _generate_from_mapping(project_id: str, drs_type: DrsType,
                           mapping: dict[str, str]) -> DrsGenerationReport:
    if project_id in GENERATORS:
        return GENERATORS[project_id].generate_from_mapping(mapping=mapping, drs_type=drs_type)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"project '{project_id}' not available")


def _generate_from_terms(project_id: str, drs_type: DrsType,
                         terms: list[str]) -> DrsGenerationReport:
    if project_id in GENERATORS:
        return GENERATORS[project_id].generate_from_bag_of_terms(terms=terms,
                                                                 drs_type=drs_type)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"project '{project_id}' not available")


def _validate(project_id: str, drs_type: DrsType, expression: str) -> DrsValidationReport:
    if project_id in VALIDATORS:
        return VALIDATORS[project_id].validate(drs_expression=expression, drs_type=drs_type)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"project '{project_id}' not available")


@router.get('/{project_id}/validation/directory',
            summary="Validate an expression against the DRS directory specification of a given project",
            description=generate_route_desc(f'{DRS_VAL_PREFIX}.validate_directory'))
async def validate_directory(
        project_id: Annotated[str, Path(description="an id of a project")],
        expression: Annotated[str, Query(description="The DRS expression to be validated")]) \
                                                                            -> DrsValidationReport:
    result = _validate(project_id=project_id, drs_type=DrsType.DIRECTORY, expression=expression)
    return result


@router.get('/{project_id}/validation/filename',
            summary="Validate an expression against the DRS file name specification of a given project",
            description=generate_route_desc(f'{DRS_VAL_PREFIX}.validate_file_name'))
async def validate_file_name(
        project_id: Annotated[str, Path(description="an id of a project")],
        expression: Annotated[str, Query(description="The DRS expression to be validated")]) \
                                                                            -> DrsValidationReport:
    return _validate(project_id=project_id, drs_type=DrsType.FILE_NAME, expression=expression)


@router.get('/{project_id}/validation/datasetid',
            summary="Validate an expression against the DRS dataset id specification of a given project",
            description=generate_route_desc(f'{DRS_VAL_PREFIX}.validate_dataset_id'))
async def validate_dataset_id(
        project_id: Annotated[str, Path(description="an id of a project")],
        expression: Annotated[str, Query(description="The DRS expression to be validated")]) \
                                                                            -> DrsValidationReport:
    return _validate(project_id=project_id, drs_type=DrsType.DATASET_ID, expression=expression)


@router.post('/{project_id}/generation/mapping/directory',
             summary='Generate a DRS directory path for a given project from a mapping of ' +
                     'collections and terms',
             description=generate_route_desc(f'{DRS_GEN_PREFIX}.generate_directory_from_mapping'))
async def generate_directory_from_mapping(
        project_id: Annotated[str, Path(description="an id of a project")],
        mapping: dict[str, str]) -> DrsGenerationReport:
    return _generate_from_mapping(project_id=project_id, drs_type=DrsType.DIRECTORY, mapping=mapping)


@router.post('/{project_id}/generation/mapping/filename',
             summary='Generate a DRS file name for a given project from a mapping of ' +
                     'collections and terms',
             description=generate_route_desc(f'{DRS_GEN_PREFIX}.generate_file_name_from_mapping'))
async def generate_file_name_from_mapping(
        project_id: Annotated[str, Path(description="an id of a project")],
        mapping: dict[str, str]) -> DrsGenerationReport:
    return _generate_from_mapping(project_id=project_id, drs_type=DrsType.FILE_NAME, mapping=mapping)


@router.post('/{project_id}/generation/mapping/datasetid',
             summary='Generate a DRS dataset id for a given project from a mapping of ' +
                     'collections and terms',
             description=generate_route_desc(f'{DRS_GEN_PREFIX}.generate_dataset_id_from_mapping'))
async def generate_dataset_id_from_mapping(
        project_id: Annotated[str, Path(description="an id of a project")],
        mapping: dict[str, str]) -> DrsGenerationReport:
    return _generate_from_mapping(project_id=project_id, drs_type=DrsType.DATASET_ID, mapping=mapping)


@router.post('/{project_id}/generation/terms/directory',
             summary='Generate a DRS directory path for a given project from a bag of terms',
             description=generate_route_desc(f'{DRS_GEN_PREFIX}.generate_directory_from_bag_of_terms'))
async def generate_directory_from_bag_of_terms(
        project_id: Annotated[str, Path(description="an id of a project")],
        terms: list[str]) -> DrsGenerationReport:
    return _generate_from_terms(project_id=project_id, drs_type=DrsType.DIRECTORY, terms=terms)


@router.post('/{project_id}/generation/terms/filename',
             summary='Generate a DRS file name for a given project from a bag of terms',
             description=generate_route_desc(f'{DRS_GEN_PREFIX}.generate_file_name_from_bag_of_terms'))
async def generate_file_name_from_bag_of_terms(
        project_id: Annotated[str, Path(description="an id of a project")],
        terms: list[str]) -> DrsGenerationReport:
    return _generate_from_terms(project_id=project_id, drs_type=DrsType.FILE_NAME, terms=terms)


@router.post('/{project_id}/generation/terms/datasetid',
             summary='Generate a DRS dataset id for a given project from a bag of terms',
             description=generate_route_desc(f'{DRS_GEN_PREFIX}.generate_dataset_id_from_bag_of_terms'))
async def generate_dataset_id_from_bag_of_terms(
        project_id: Annotated[str, Path(description="an id of a project")],
        terms: list[str]) -> DrsGenerationReport:
    return _generate_from_terms(project_id=project_id, drs_type=DrsType.DATASET_ID, terms=terms)
