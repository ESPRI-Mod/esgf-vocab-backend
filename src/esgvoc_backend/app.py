import time

from fastapi import FastAPI, Request

import esgvoc_backend.drs as drs
import esgvoc_backend.index as index
import esgvoc_backend.projects as projects
import esgvoc_backend.universe as universe
import esgvoc_backend.uris as uris


async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000.
    response.headers["X-Process-Time"] = f'{process_time:.1f} ms'
    return response


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(universe.router)
    app.include_router(projects.router)
    app.include_router(drs.router)
    app.include_router(uris.router)
    app.include_router(index.router)
    app.middleware("http")(add_process_time_header)
    return app


app = create_app()
