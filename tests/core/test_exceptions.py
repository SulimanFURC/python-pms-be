from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.exceptions import AppException, register_exception_handlers


def create_test_app() -> FastAPI:
    """Create an isolated FastAPI application for exception testing."""

    test_app = FastAPI()
    register_exception_handlers(test_app)

    @test_app.get("/test/default-error")
    async def default_error() -> None:
        raise AppException("Invalid request.")

    @test_app.get("/test/custom-error")
    async def custom_error() -> None:
        raise AppException(
            message="Access denied.",
            status_code=403,
            code="forbidden",
        )

    @test_app.get("/test/unexpected-error")
    async def unexpected_error() -> None:
        raise RuntimeError("Sensitive internal error.")

    return test_app


def test_app_exception_default_status_code() -> None:
    """Verify the default status code for AppException."""

    with TestClient(create_test_app()) as client:
        response = client.get("/test/default-error")

    assert response.status_code == 400


def test_app_exception_custom_status_and_response() -> None:
    """Verify custom status codes and structured error responses."""

    with TestClient(create_test_app()) as client:
        response = client.get("/test/custom-error")

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Access denied.",
        "code": "forbidden",
    }


def test_app_exception_default_response() -> None:
    """Verify the default application exception response."""

    with TestClient(create_test_app()) as client:
        response = client.get("/test/default-error")

    assert response.json() == {
        "detail": "Invalid request.",
        "code": "application_error",
    }


def test_unhandled_exception_response() -> None:
    """Verify unexpected exceptions return a generic HTTP 500 response."""

    with TestClient(
        create_test_app(),
        raise_server_exceptions=False,
    ) as client:
        response = client.get("/test/unexpected-error")

    assert response.status_code == 500
    assert response.json() == {
        "detail": "An unexpected error occurred.",
        "code": "internal_server_error",
    }
