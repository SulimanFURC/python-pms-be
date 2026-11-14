
# Project Management System (PMS)

A production-oriented Project Management System REST API built with FastAPI, PostgreSQL, SQLAlchemy 2.0, and Docker.

## 1. Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.12+ |
| API Framework | FastAPI |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 (Async) |
| Database Driver | asyncpg |
| Migrations | Alembic |
| Configuration | Pydantic Settings |
| Testing | pytest, HTTPX |
| Code Quality | Ruff, mypy |
| Containerization | Docker, Docker Compose |

## 2. Project Architecture

```text
pms/
├── app/
│   ├── api/
│   │   └── health.py
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── modules/
│   └── main.py
├── migrations/
│   └── versions/
├── tests/
│   ├── api/
│   ├── core/
│   └── conftest.py
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

### Application layers

- `api/`: HTTP routes and API endpoints.
- `core/`: Application configuration, logging, and exception handling.
- `db/`: Database engine, session management, and ORM base.
- `modules/`: Feature-specific business modules.
- `migrations/`: Alembic database migration scripts.
- `tests/`: Automated tests.

## 3. Prerequisites

For local development:

- Python 3.12 or newer
- PostgreSQL 16, or Docker Desktop
- Git

For containerized development:

- Docker Desktop
- Docker Compose v2

## 4. Local Development Setup

### Clone the repository

```bash
git clone <repository-url>
cd pms
```

### Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

### Configure environment variables

Copy the example configuration:

```powershell
Copy-Item .env.example .env
```

Update `.env` with your local PostgreSQL credentials.

For local development, the database connection uses the host and port configured in `DATABASE_URL`.

### Start the API

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

http://localhost:8000

## 5. Docker Development Setup

Docker Compose starts the API and PostgreSQL services together.

### Start services

```powershell
docker compose up -d --build
```

### Check container status

```powershell
docker compose ps
```

### View application logs

```powershell
docker compose logs -f app
```

### View database logs

```powershell
docker compose logs -f db
```

### Stop services

```powershell
docker compose down
```

The PostgreSQL data is stored in the persistent `postgres_data` Docker volume.

Do not use `docker compose down -v` unless you intentionally want to delete the database volume and its data.

### Docker networking

The API container connects to PostgreSQL through the Compose service hostname:

```text
db:5432
```

When running the API directly on the host, use the configured host database address, normally:

```text
localhost:5433
```

## 6. API Endpoints

### Health check

```http
GET /health
```

Checks whether the application process is running.

Example response:

```json
{
  "status": "ok"
}
```

### Database readiness check

```http
GET /health/ready
```

Checks whether the application can communicate with PostgreSQL.

Example response:

```json
{
  "status": "ok",
  "database": "connected"
}
```

Returns HTTP 503 when the database is unavailable.

## 7. API Documentation

FastAPI provides interactive API documentation.

| Documentation | URL |
|---|---|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| OpenAPI Schema | http://localhost:8000/openapi.json |

## 8. Database Migrations

Alembic manages database schema migrations.

Create a migration:

```powershell
alembic revision --autogenerate -m "migration description"
```

Apply migrations:

```powershell
alembic upgrade head
```

Check the current migration:

```powershell
alembic current
```

View migration history:

```powershell
alembic history
```

Run Alembic commands in the environment where the database URL is correctly configured.

## 9. Testing

Run the complete test suite:

```powershell
python -m pytest -v
```

Run tests with coverage:

```powershell
python -m pytest --cov=app --cov-report=term-missing
```

## 10. Code Quality

Format source code:

```powershell
python -m ruff format app tests
```

Check formatting:

```powershell
python -m ruff format --check app tests
```

Run linting:

```powershell
python -m ruff check app tests
```

Run static type checking:

```powershell
python -m mypy app tests
```

## 11. Environment Variables

| Variable | Purpose |
|---|---|
| `APP_NAME` | Application name |
| `APP_ENV` | Environment: development, production, or testing |
| `DEBUG` | Enables or disables debug mode |
| `API_V1_PREFIX` | Versioned API prefix |
| `POSTGRES_DB` | PostgreSQL database name |
| `POSTGRES_USER` | PostgreSQL username |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `POSTGRES_PORT` | Host port mapped to PostgreSQL |
| `DATABASE_URL` | SQLAlchemy asynchronous database URL |
| `APP_PORT` | Host port mapped to the API container |

Never commit `.env` files or production credentials to version control.

## 12. Development Roadmap

The project is being implemented in the following milestones:

1. Project Foundation
2. Authentication & User Management
3. Organizations & Membership
4. Authorization & Multi-tenancy
5. Project Management
6. Task Management
7. Collaboration
8. Milestones & Activity Tracking
9. Notifications
10. Dashboard & Reporting
11. Testing & Performance
12. Production Deployment

## 13. Current Implementation Status

Project Foundation includes:

- Git repository and Python environment
- Dependency management
- Application architecture
- Centralized configuration
- PostgreSQL Docker service
- SQLAlchemy asynchronous integration
- Alembic migration setup
- FastAPI application
- Health and readiness endpoints
- Structured logging and exception handling
- Automated tests
- Dockerized API application
- Project documentation

---

**Project:** Project Management System  
**Status:** Foundation milestone nearing completion  
**Python:** 3.12+
