uvicorn:
	uv run uvicorn esgvoc_backend.app:app --port=9999 --reload --loop=asyncio --http=httptools

gunicorn:
	uv run gunicorn -k uvicorn_worker.UvicornWorker  esgvoc_backend.app:app
