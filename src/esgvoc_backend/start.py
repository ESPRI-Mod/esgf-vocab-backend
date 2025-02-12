import logging
import os

import uvicorn

# This import the logging settings of the library ESGVOC.

_DEFAULT_NB_WORKERS = 1
_UVICORN_WORKERS_VAR_ENV_NAME = "WEB_CONCURRENCY"
_UVICORN_PORT = 9999
_APP = "esgvoc_backend.app:app"
# Set the root level at INFO (ESGVOC set it at ERROR).
logging.getLogger().setLevel(logging.INFO)
_LOGGER = logging.getLogger("start")

def main():
    n_workers = (
        int(os.environ[_UVICORN_WORKERS_VAR_ENV_NAME])
        if _UVICORN_WORKERS_VAR_ENV_NAME in os.environ
        else _DEFAULT_NB_WORKERS
    )
    _LOGGER.info(f"number of uvicorn workers: {n_workers}")

    uvicorn.run(
        app=_APP,
        host="0.0.0.0",
        port=_UVICORN_PORT,
        proxy_headers=True,
        forwarded_allow_ips="*",
        reload=False,
        workers=n_workers,
    )
