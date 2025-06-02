import logging
import logging.config
import time

from esgvoc.core.exceptions import EsgvocNotFoundError, EsgvocValueError
from fastapi import FastAPI, HTTPException, Request, status
from uvicorn_worker import UvicornWorker

from esgvoc_backend import constants, cross, drs, index, projects, search, universe, update, uris, validation

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'esgvoc_backend_formatter': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
    },
    'handlers': {
        'esgvoc_backend_stdout': {
            'class': 'logging.StreamHandler',
            'formatter': 'esgvoc_backend_formatter',
        },
    },
    'loggers': {
        'esgvoc_backend': {
            'handlers': ['esgvoc_backend_stdout'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}

logging.config.dictConfig(logging_config)


async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000.
    response.headers["X-Process-Time"] = f'{process_time:.1f} ms'
    return response


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(universe.router, prefix=constants.API_PREFIX)
    app.include_router(projects.router, prefix=constants.API_PREFIX)
    app.include_router(drs.router, prefix=constants.API_PREFIX)
    app.include_router(search.router, prefix=constants.API_PREFIX)
    app.include_router(validation.router, prefix=constants.API_PREFIX)
    app.include_router(cross.router, prefix=constants.API_PREFIX)
    app.include_router(update.router, prefix=constants.API_PREFIX)
    app.include_router(uris.router)
    app.include_router(index.router)
    app.middleware("http")(add_process_time_header)
    return app


app = create_app()

# Configure the ESGVOC library logger.
logging.getLogger(constants.ESGVOC_ROOT_LOGGER_NAME).setLevel(constants.LOG_LEVEL)


@app.exception_handler(EsgvocValueError)
async def esgvoc_value_error_handler(_: Request, e: EsgvocValueError):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@app.exception_handler(EsgvocNotFoundError)
async def esgvoc_not_found_error_handler(_: Request, e: EsgvocNotFoundError):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


# When running with GUnicorn and Uvicorn worker,
# the default uvloop causes this error: "Error while closing socket [Errno 9] Bad file descriptor".
# Fix is to stick the classical with asyncio loop.
class EsgvocUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {"loop": "asyncio"}
