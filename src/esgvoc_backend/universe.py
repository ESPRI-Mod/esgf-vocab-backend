from typing import Annotated

import esgvoc.api.universe as universe
from esgvoc.api.data_descriptors.data_descriptor import DataDescriptor
from esgvoc.api.search import SearchSettings
from fastapi import APIRouter, Query

router = APIRouter(prefix="/universe")

"""
/universe/terms              => get_all_terms_in_universe
/universe/terms/find?term_id => find_terms_in_universe

/universe/data_descriptors                         => get_all_data_descriptors_in_universe
/universe/data_descriptors/find?data_descriptor_id => find_data_descriptors_in_universe

/universe/data_descriptors/{data_descriptor_id}/terms              => get_all_terms_in_data_descriptor
/universe/data_descriptors/{data_descriptor_id}/terms/find?term_id => find_terms_in_data_descriptor
"""


@router.get("/terms", summary="Get all the terms of the universe")
async def get_terms_from_universe(
    selected_term_fields: Annotated[
        list[str] | None, Query(description="Selected term fields or null")
    ] = None,
) -> list[DataDescriptor]:
    return universe.get_all_terms_in_universe(selected_term_fields=selected_term_fields)


@router.get("/terms/find", summary="Find terms in the universe")
async def find_terms_from_universe(
    term_id: Annotated[str, Query(description="The terms to be found")],
    settings: SearchSettings | None = None,
) -> list[DataDescriptor]:
    return universe.find_terms_in_universe(term_id=term_id, settings=settings)


@router.get("/data_descriptors", summary="Get all the data descriptor contexts")
async def get_data_descriptors() -> list[str]:
    return universe.get_all_data_descriptors_in_universe()
