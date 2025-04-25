from typing import Annotated

import esgvoc.api.universe as universe
from esgvoc.api.data_descriptors.data_descriptor import DataDescriptor
from fastapi import APIRouter, Path, Query
from pydantic import SerializeAsAny

from esgvoc_backend.naming import UNIVERSE_PAGE_PREFIX
from esgvoc_backend.utils import check_result, generate_route_desc

router = APIRouter(prefix="/universe")


@router.get("/terms",
            summary="Get all terms of the universe",
            description=generate_route_desc(f'{UNIVERSE_PAGE_PREFIX}.get_all_terms_in_universe'))
async def get_all_terms_in_universe(
    selected_term_fields: Annotated[list[str] | None,
                                    Query(description="list of selected term fields, empty or null")] = None) \
                                                            -> list[SerializeAsAny[DataDescriptor]]:
    return universe.get_all_terms_in_universe(selected_term_fields=selected_term_fields)


@router.get("/terms/{term_id}",
            summary="Get a term of the universe",
            description=generate_route_desc(f'{UNIVERSE_PAGE_PREFIX}.get_term_in_universe'))
async def get_term_in_universe(
    term_id: Annotated[str, Path(description="an id of a term")],
    selected_term_fields: Annotated[list[str] | None,
                                    Query(description="list of selected term fields, empty or null")] = None) \
                                                                  -> SerializeAsAny[DataDescriptor]:
    result = universe.get_term_in_universe(term_id=term_id, selected_term_fields=selected_term_fields)
    return check_result(result)


@router.get("/data_descriptors",
            summary="Get all the data descriptors",
            description=generate_route_desc(f'{UNIVERSE_PAGE_PREFIX}.get_all_data_descriptors_in_universe'))
async def get_all_data_descriptors_in_universe() -> list[str]:
    return universe.get_all_data_descriptors_in_universe()


@router.get("/data_descriptors/{data_descriptor_id}",
            summary="Get a data descriptor of the universe",
            description=generate_route_desc(f'{UNIVERSE_PAGE_PREFIX}.get_data_descriptor_in_universe'))
async def get_data_descriptor_in_universe(
    data_descriptor_id: Annotated[str, Path(description="an id of a data descriptor")]) \
                                                                                -> tuple[str, dict]:
    result = universe.get_data_descriptor_in_universe(data_descriptor_id=data_descriptor_id)
    return check_result(result)


@router.get("/data_descriptors/{data_descriptor_id}/terms",
            summary="Get all terms of a given data descriptor",
            description=generate_route_desc(f'{UNIVERSE_PAGE_PREFIX}.get_all_terms_in_data_descriptor'))
async def get_all_terms_in_data_descriptor(
    data_descriptor_id: Annotated[str, Path(description="an id of a data descriptor")],
    selected_term_fields: Annotated[list[str] | None,
                                    Query(description="list of selected term fields, empty or null")] = None) \
                                                            -> list[SerializeAsAny[DataDescriptor]]:
    result = universe.get_all_terms_in_data_descriptor(data_descriptor_id=data_descriptor_id,
                                                       selected_term_fields=selected_term_fields)
    return check_result(result)


@router.get("/data_descriptors/{data_descriptor_id}/terms/{term_id}",
            summary="Get a term of a given data descriptor",
            description=generate_route_desc(f'{UNIVERSE_PAGE_PREFIX}.get_term_in_data_descriptor'))
async def get_term_in_data_descriptor(
    data_descriptor_id: Annotated[str, Path(description="an id of a data descriptor")],
    term_id: Annotated[str, Path(description="an id of a term")],
    selected_term_fields: Annotated[list[str] | None,
                                    Query(description="list of selected term fields, empty or null")] = None) \
                                                                  -> SerializeAsAny[DataDescriptor]:
    result = universe.get_term_in_data_descriptor(data_descriptor_id=data_descriptor_id,
                                                  term_id=term_id,
                                                  selected_term_fields=selected_term_fields)
    return check_result(result)
