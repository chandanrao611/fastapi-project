from fastapi import HTTPException
from typing import Any, List
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.Response import Response

# HTTP errors (404, 401, etc.)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return Response.error(
        message=exc.detail,
        status_code=exc.status_code
    )

# Validation errors (Pydantic)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return Response.error(
        message="Validation Error",
        status_code=422,
        data=get_messages(exc)
    )


# 🔥 Catch ALL errors (MOST IMPORTANT)
async def global_exception_handler(request: Request, exc: Exception):
    print("🔥 ERROR:", exc)  # debug log
    return Response.error(
        message="Internal Server Error",
        status_code=500
    )

def get_messages(exc: Any) -> List[str]:

    # ✅ Validation Errors (multiple)
    if isinstance(exc, RequestValidationError):
        errors = exc.errors()
        return [
            f"{err.get('loc')[-1]}: {err.get('msg')}"
            for err in errors
        ]

    # ✅ HTTPException
    if isinstance(exc, HTTPException):
        if isinstance(exc.detail, list):
            return [str(msg) for msg in exc.detail]
        return [str(exc.detail)]

    # ✅ Custom exception with detail
    if hasattr(exc, "detail"):
        if isinstance(exc.detail, list):
            return [str(msg) for msg in exc.detail]
        return [str(exc.detail)]

    # ✅ Generic Exception
    if isinstance(exc, Exception):
        return [str(exc)]

    return ["Unknown error"]