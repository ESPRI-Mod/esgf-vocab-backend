from typing import Annotated

import esgvoc.api.universe as universe
from esgvoc.api.data_descriptors.data_descriptor import DataDescriptor
from esgvoc.api.search import SearchSettings
from fastapi import APIRouter, Path, Query
from pydantic import SerializeAsAny

from esgvoc_backend.utils import _generate_route_desc

# Prefix for the API Web documentation of the route.
_PAGE_PREFIX = 'universe.html#esgvoc.api.universe'

router = APIRouter(prefix="/universe")

"""
/universe/terms              => get_all_terms_in_universe
/universe/terms/find?term_id => find_terms_in_universe

/universe/data_descriptors                         => get_all_data_descriptors_in_universe
/universe/data_descriptors/find?data_descriptor_id => find_data_descriptors_in_universe

/universe/data_descriptors/{data_descriptor_id}/terms              => get_all_terms_in_data_descriptor
/universe/data_descriptors/{data_descriptor_id}/terms/find?term_id => find_terms_in_data_descriptor
"""


@router.get("/terms",
            summary="Get all terms of the universe",
            description=_generate_route_desc(f'{_PAGE_PREFIX}.get_all_terms_in_universe'))
async def get_terms_in_universe(
        selected_term_fields: Annotated[list[str] | None,
                                        Query(description="Selected term fields or null")] = None) \
                                                            -> list[SerializeAsAny[DataDescriptor]]:
    return universe.get_all_terms_in_universe(selected_term_fields=selected_term_fields)


@router.post("/terms/find",
             summary="Find terms in the universe",
             description=_generate_route_desc(f'{_PAGE_PREFIX}.find_terms_in_universe'))
async def find_terms_in_universe(
        term_id: Annotated[str, Query(description="The terms to be found")],
        settings: SearchSettings | None = None) -> list[SerializeAsAny[DataDescriptor]]:
    return universe.find_terms_in_universe(term_id=term_id, settings=settings)


@router.get("/data_descriptors",
            summary="Get all the data descriptors",
            description=_generate_route_desc(f'{_PAGE_PREFIX}.get_all_data_descriptors_in_universe'))
async def get_data_descriptors() -> list[str]:
    return universe.get_all_data_descriptors_in_universe()


@router.post("/data_descriptors/find",
             summary="Find data descriptors in the universe",
             description=_generate_route_desc(f'{_PAGE_PREFIX}.find_data_descriptors_in_universe'))
async def find_data_descriptors(
        data_descriptor_id: Annotated[str, Query(description="The data descriptors to be found")],
        settings: SearchSettings | None = None) -> list[dict]:
    return universe.find_data_descriptors_in_universe(data_descriptor_id=data_descriptor_id,
                                                      settings=settings)


@router.get("/data_descriptors/{data_descriptor_id}/terms",
            summary="Get all terms of a given data descriptor",
            description=_generate_route_desc(f'{_PAGE_PREFIX}.get_all_terms_in_data_descriptor'))
async def get_terms_in_data_descriptor(
        data_descriptor_id: Annotated[str, Path(description="The given data descriptor")],
        selected_term_fields: Annotated[list[str] | None,
                                        Query(description="Selected term fields or null")] = None) \
                                                            -> list[SerializeAsAny[DataDescriptor]]:
    return universe.get_all_terms_in_data_descriptor(data_descriptor_id=data_descriptor_id,
                                                     selected_term_fields=selected_term_fields)


@router.post("/data_descriptors/{data_descriptor_id}/terms/find",
             summary="Find terms in a given data descriptor",
             description=_generate_route_desc(f'{_PAGE_PREFIX}.find_terms_in_data_descriptor'))
async def find_terms_in_data_descriptors(
        data_descriptor_id: Annotated[str, Path(description="The given data descriptor")],
        term_id: Annotated[str, Query(description="The terms to be found")],
        settings: SearchSettings | None = None) -> list[SerializeAsAny[DataDescriptor]]:
    return universe.find_terms_in_data_descriptor(data_descriptor_id=data_descriptor_id,
                                                  term_id=term_id,
                                                  settings=settings)
