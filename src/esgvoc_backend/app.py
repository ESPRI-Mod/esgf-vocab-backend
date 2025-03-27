import time

from esgvoc.core.exceptions import EsgvocNotFoundError, EsgvocValueError
from fastapi import FastAPI, HTTPException, Request, status

from esgvoc_backend import drs, index, naming, projects, search, universe, uris, validation


async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000.
    response.headers["X-Process-Time"] = f'{process_time:.1f} ms'
    return response


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(universe.router, prefix=naming.API_PREFIX)
    app.include_router(projects.router, prefix=naming.API_PREFIX)
    app.include_router(drs.router, prefix=naming.API_PREFIX)
    app.include_router(search.router, prefix=naming.API_PREFIX)
    app.include_router(validation.router, prefix=naming.API_PREFIX)
    app.include_router(uris.router)
    app.include_router(index.router)
    app.middleware("http")(add_process_time_header)
    return app


app = create_app()


@app.exception_handler(EsgvocValueError)
async def esgvoc_value_error_handler(_: Request, e: EsgvocValueError):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@app.exception_handler(EsgvocNotFoundError)
async def esgvoc_not_found_error_handler(_: Request, e: EsgvocNotFoundError):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
