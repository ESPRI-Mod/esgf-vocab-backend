from typing import Annotated

import esgvoc.api.universe as universe
from esgvoc.api._utils import Item
from esgvoc.api.data_descriptors.data_descriptor import DataDescriptor
from fastapi import APIRouter, Path, Query
from pydantic import SerializeAsAny

from esgvoc_backend.naming import _generate_route_desc

# Prefix for the API Web documentation of the route.
_PAGE_PREFIX = 'universe.html#esgvoc.api.universe'

router = APIRouter(prefix="/universe")

"""
/universe/items/find?expression&only_id => find_items_in_universe

/universe/terms                         => get_all_terms_in_universe
/universe/terms/get?term_id             => get_term_in_universe
/universe/terms/find?expression&only_id => find_terms_in_universe

/universe/data_descriptors                         => get_all_data_descriptors_in_universe
/universe/data_descriptors/get?data_descriptor_id  => get_data_descriptor_in_universe
/universe/data_descriptors/find?expression&only_id => find_data_descriptors_in_universe

/universe/data_descriptors/{data_descriptor_id}/terms                         => get_all_terms_in_data_descriptor
/universe/data_descriptors/{data_descriptor_id}/terms/get?term_id             => get_term_in_data_descriptor
/universe/data_descriptors/{data_descriptor_id}/terms/find?expression&only_id => find_terms_in_data_descriptor
"""


@router.get("/items/find",
            summary="Find items of the universe",
            description=_generate_route_desc(f'{_PAGE_PREFIX}.find_items_in_universe'))
async def find_items_in_universe(
    expression: Annotated[str, Query(description="keywords and boolean operators")],
    only_id: Annotated[bool, Query(description="search in id otherwise all specifications")] = False) \
                                                            -> list[Item]:
    return universe.find_items_in_universe(expression=expression, only_id=only_id)


@router.get("/terms",
            summary="Get all terms of the universe",
            description=_generate_route_desc(f'{_PAGE_PREFIX}.get_all_terms_in_universe'))
async def get_terms_in_universe(
        selected_term_fields: Annotated[list[str] | None,
                                        Query(description="list of selected term fields, empty or null")] = None) \
                                                            -> list[SerializeAsAny[DataDescriptor]]:
    return universe.get_all_terms_in_universe(selected_term_fields=selected_term_fields)


@router.get("/terms/get",
            summary="Get a term of the universe",
            description=_generate_route_desc(f'{_PAGE_PREFIX}.get_term_in_universe'))
async def get_term_in_universe(
        term_id: Annotated[str, Query(description="An id of a term")],
        selected_term_fields: Annotated[list[str] | None,
                                        Query(description="list of selected term fields, empty or null")] = None) \
                                                            -> SerializeAsAny[DataDescriptor] | None:
    return universe.get_term_in_universe(term_id=term_id, selected_term_fields=selected_term_fields)


@router.get("/terms/find",
            summary="Find terms in the universe",
            description=_generate_route_desc(f'{_PAGE_PREFIX}.find_terms_in_universe'))
async def find_terms_in_universe(
        expression: Annotated[str, Query(description="keywords and boolean operators")],
        only_id: Annotated[bool, Query(description="search in id otherwise all specifications")] = False,
        selected_term_fields: Annotated[list[str] | None,
                                        Query(description="list of selected term fields, empty or null")] = None) \
                                                            -> list[SerializeAsAny[DataDescriptor]]:
    return universe.Rfind_terms_in_universe(expression=expression, only_id=only_id,
                                            selected_term_fields=selected_term_fields)


@router.get("/data_descriptors",
            summary="Get all the data descriptors",
            description=_generate_route_desc(f'{_PAGE_PREFIX}.get_all_data_descriptors_in_universe'))
async def get_data_descriptors() -> list[str]:
    return universe.get_all_data_descriptors_in_universe()


@router.get("/data_descriptors/get",
            summary="Get a data descriptor of the universe",
            description=_generate_route_desc(f'{_PAGE_PREFIX}.get_data_descriptor_in_universe'))
async def get_data_descriptor_in_universe(
    data_descriptor_id: Annotated[str, Query(description="An id of a data descriptor")]) \
        -> tuple[str, dict] | None:
    return universe.get_data_descriptor_in_universe(data_descriptor_id=data_descriptor_id)


@router.get("/data_descriptors/find",
            summary="Find data descriptors in the universe",
            description=_generate_route_desc(f'{_PAGE_PREFIX}.find_data_descriptors_in_universe'))
async def find_data_descriptors(
        expression: Annotated[str, Query(description="keywords and boolean operators")],
        only_id: Annotated[bool, Query(description="search in id otherwise all specifications")] = False) \
                                                                          -> list[tuple[str, dict]]:
    return universe.Rfind_data_descriptors_in_universe(expression=expression, only_id=only_id)


@router.get("/data_descriptors/{data_descriptor_id}/terms",
            summary="Get all terms of a given data descriptor",
            description=_generate_route_desc(f'{_PAGE_PREFIX}.get_all_terms_in_data_descriptor'))
async def get_terms_in_data_descriptor(
        data_descriptor_id: Annotated[str, Path(description="The given data descriptor")],
        selected_term_fields: Annotated[list[str] | None,
                                        Query(description="list of selected term fields, empty or null")] = None) \
                                                            -> list[SerializeAsAny[DataDescriptor]]:
    return universe.get_all_terms_in_data_descriptor(data_descriptor_id=data_descriptor_id,
                                                     selected_term_fields=selected_term_fields)


@router.get("/data_descriptors/{data_descriptor_id}/terms/get",
            summary="Get a terms of a given data descriptor",
            description=_generate_route_desc(f'{_PAGE_PREFIX}.get_term_in_data_descriptor'))
async def get_term_in_data_descriptor(
        data_descriptor_id: Annotated[str, Path(description="An id of a data descriptor")],
        term_id: Annotated[str, Query(description="The id of a term")],
        selected_term_fields: Annotated[list[str] | None,
                                        Query(description="list of selected term fields, empty or null")] = None) \
                                                            -> SerializeAsAny[DataDescriptor] | None:
    return universe.get_term_in_data_descriptor(data_descriptor_id=data_descriptor_id,
                                                term_id=term_id,
                                                selected_term_fields=selected_term_fields)


@router.get("/data_descriptors/{data_descriptor_id}/terms/find",
            summary="Find terms in a given data descriptor",
            description=_generate_route_desc(f'{_PAGE_PREFIX}.find_terms_in_data_descriptor'))
async def find_terms_in_data_descriptors(
        expression: Annotated[str, Query(description="keywords and boolean operators")],
        data_descriptor_id: Annotated[str, Path(description="An id of a data descriptor")],
        only_id: Annotated[bool, Query(description="search in id otherwise all specifications")] = False,
        selected_term_fields: Annotated[list[str] | None,
                                        Query(description="list of selected term fields, empty or null")] = None) \
                                                            -> list[SerializeAsAny[DataDescriptor]]:
    return universe.Rfind_terms_in_data_descriptor(expression=expression,
                                                   data_descriptor_id=data_descriptor_id,
                                                   only_id=only_id,
                                                   selected_term_fields=selected_term_fields)
