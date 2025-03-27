from typing import Any

from fastapi import HTTPException, status


def check_result(result: Any | None) -> Any:
    if result:
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
