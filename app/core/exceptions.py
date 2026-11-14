import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Base exception for application-specific errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        code: str = "application_error",
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.code = code
        super().__init__(message)


async def app_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle expected application-specific exceptions."""

    assert isinstance(exc, AppException), "app_exception_handler must receive an AppException"

    logger.warning(
        "Application error: %s | Path: %s",
        exc.code,
        request.url.path,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "code": exc.code,
        },
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle unexpected application exceptions."""

    logger.exception(
        "Unhandled exception | Method: %s | Path: %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred.",
            "code": "internal_server_error",
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register application-wide exception handlers."""

    app.add_exception_handler(
        AppException,
        app_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        unhandled_exception_handler,
    )
