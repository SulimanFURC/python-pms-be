from collections.abc import AsyncIterator
from typing import cast

from fastapi.testclient import TestClient
from sqlalchemy import Executable
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.main import app


class FakeDatabaseSession:
    """Simulate an asynchronous database session."""

    def __init__(self, error: SQLAlchemyError | None = None) -> None:
        self.error = error
        self.executed_statements: list[str] = []

    async def execute(self, statement: Executable) -> None:
        self.executed_statements.append(str(statement))

        if self.error is not None:
            raise self.error


def override_database(db: FakeDatabaseSession) -> None:
    """Override the database dependency with a fake session."""

    async def get_test_db() -> AsyncIterator[AsyncSession]:
        yield cast(AsyncSession, db)

    app.dependency_overrides[get_db] = get_test_db


def test_health_check(client: TestClient) -> None:
    """Verify that the application liveness endpoint works."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_check_success(client: TestClient) -> None:
    """Verify database readiness when the database is available."""

    fake_db = FakeDatabaseSession()
    override_database(fake_db)

    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "database": "connected",
    }
    assert fake_db.executed_statements == ["SELECT 1"]


def test_readiness_check_failure(client: TestClient) -> None:
    """Verify database readiness when the database is unavailable."""

    fake_db = FakeDatabaseSession(error=SQLAlchemyError("Database connection failed"))
    override_database(fake_db)

    response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {
        "detail": {
            "status": "not_ready",
            "database": "unavailable",
        }
    }
