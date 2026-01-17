FROM --platform=$TARGETPLATFORM python:3.13-slim

ARG ENV_PATH=.env.local

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

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

RUN uv sync --locked

EXPOSE 9010
ENV UV_ENV_FILE=.env

CMD ["uv", "run", "src/mlflow_service.py", "-p", "9010"]
