from typing import Annotated

from fastapi import APIRouter, Path
from fastapi.responses import Response

from esgvoc_backend.cache import STAC_JSON_SCHEMAS
from esgvoc_backend.constants import JSG_PREFIX
from esgvoc_backend.utils import check_result, generate_route_desc

router = APIRouter(prefix="/apps/jsg")


@router.get("/{project_id}",
            summary="Get a STAC JSON schema",
            description=generate_route_desc(f'{JSG_PREFIX}.generate_json_schema'))
async def generate_json_schema(project_id: Annotated[str, Path(description="an id of a project")]) \
                                                                                        -> Response:
    result = None
    if project_id in STAC_JSON_SCHEMAS:
        result = STAC_JSON_SCHEMAS[project_id]
    return Response(content=check_result(result), media_type="application/json")
