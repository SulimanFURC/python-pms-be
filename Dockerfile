
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-root application user.
RUN groupadd --system app && \
    useradd --system --gid app --create-home app

# Install the application and its dependencies.
COPY pyproject.toml ./
COPY app ./app

RUN pip install --no-cache-dir .

# Include Alembic configuration and migration scripts.
COPY alembic.ini ./
COPY migrations ./migrations

# Run the application as a non-root user.
RUN chown -R app:app /app
USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
