server:
	uv run uvicorn esgvoc_backend.app:app --port=9999 --reload --loop=asyncio --http=httptools
