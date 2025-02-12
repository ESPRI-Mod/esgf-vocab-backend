from fastapi import FastAPI

import esgvoc_backend.drs as drs
import esgvoc_backend.projects as projects
import esgvoc_backend.universe as universe
import esgvoc_backend.uris as uris


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(universe.router)
    app.include_router(projects.router)
    app.include_router(drs.router)
    app.include_router(uris.router)
    return app


app = create_app()
