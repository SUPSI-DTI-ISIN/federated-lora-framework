FROM nvcr.io/nvidia/pytorch:26.01-py3

USER root

RUN apt-get update \
    && apt-get -y --no-install-recommends install \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN id -u app &>/dev/null || useradd -m -u 49999 app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

USER app
WORKDIR /app

COPY --chown=app:app pyproject.toml uv.lock ./

RUN sed -i 's/.*flwr\[simulation\].*//' pyproject.toml

RUN uv sync --no-dev --frozen

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["flower-superexec"]