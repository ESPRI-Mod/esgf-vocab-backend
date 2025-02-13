from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

_INDEX_PAGE = '<h1>ESGVOC API Backend</h1></br>Documentation can be found <a href=docs>here</a>'


@router.get("/index.html", summary="Index page")
async def index() -> HTMLResponse:
    return HTMLResponse(_INDEX_PAGE)


@router.get("/", summary="Index page")
async def root() -> HTMLResponse:
    return HTMLResponse(_INDEX_PAGE)
