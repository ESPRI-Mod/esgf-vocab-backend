import logging
import os

from fastapi import FastAPI

import esgvoc_backend.projects as projects
import esgvoc_backend.universe as universe

_LOGGER = logging.getLogger("app")


def initialization():
    _LOGGER.info(f"initialization of process {os.getpid()}")


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(universe.router)
    app.include_router(projects.router)
    return app


initialization()
app = create_app()
