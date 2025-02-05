import logging
import os
import sys

import uvicorn

_DEFAULT_NB_WORKERS = 1
_UVICORN_WORKERS_VAR_ENV_NAME = "WEB_CONCURRENCY"
_UVICORN_PORT = 9999
_APP = "esgvoc_backend.app:app"
_LOGGER = logging.getLogger("start")

_LOG_HANDLERS = [logging.StreamHandler(sys.stdout)]
_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
_LOG_LEVEL = logging.INFO
logging.basicConfig(level=_LOG_LEVEL, format=_LOG_FORMAT, handlers=_LOG_HANDLERS)


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
