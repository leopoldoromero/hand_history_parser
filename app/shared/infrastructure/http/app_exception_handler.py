from fastapi import Request
from fastapi.responses import JSONResponse
from app.shared.domain.base_exception import BaseAppException
from app.shared.infrastructure.http.error_code_to_http_status import (
    map_error_code_to_status,
)


async def base_app_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, BaseAppException):
        return JSONResponse(
            status_code=map_error_code_to_status(exc.code), content=exc.to_dict()
        )
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "code": "INTERNAL_ERROR"},
    )
