FROM --platform=$TARGETPLATFORM nvidia/cuda:12.8.0-cudnn-runtime-ubuntu24.04

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app
COPY pyproject.toml .
COPY .python-version .

#RUN sed -i 's/.*flwr\[simulation\].*//' pyproject.toml
RUN uv python install
RUN uv sync

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["flower-superexec"]