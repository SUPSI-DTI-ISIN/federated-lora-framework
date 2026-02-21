FROM python:3.13-slim

ARG ENV_PATH=.env.local

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates netcat-openbsd

# Download UV installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

COPY src src/
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
COPY $ENV_PATH .env
COPY migrations/ migrations/
COPY alembic.ini alembic.ini
COPY docker/docker-entrypoint.sh docker-entrypoint.sh

RUN chmod +x /app/docker-entrypoint.sh

RUN uv sync

EXPOSE 9020
ENV UV_ENV_FILE=.env

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["uv", "run", "src/institute_service.py", "-p", "9020"]