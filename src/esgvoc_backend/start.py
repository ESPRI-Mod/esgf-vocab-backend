import os

import uvicorn

_DEFAULT_NB_WORKERS = 1
_UVICORN_WORKERS_VAR_ENV_NAME = "WEB_CONCURRENCY"
_UVICORN_PORT = 9999
_APP = "esgvoc_backend.app:app"


def main():
    n_workers = (
        int(os.environ[_UVICORN_WORKERS_VAR_ENV_NAME])
        if _UVICORN_WORKERS_VAR_ENV_NAME in os.environ
        else _DEFAULT_NB_WORKERS
    )

    uvicorn.run(
        app=_APP,
        host="127.0.0.1",
        port=_UVICORN_PORT,
        proxy_headers=True,
        forwarded_allow_ips="*",
        reload=False,
        workers=n_workers,
    )
