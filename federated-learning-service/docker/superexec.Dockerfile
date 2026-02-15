FROM --platform=$TARGETPLATFORM flwr/superexec:1.25.0

USER root
RUN apt-get update \
    && apt-get -y --no-install-recommends install \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

USER app

WORKDIR /app
COPY --chown=app:app pyproject.toml .
RUN sed -i 's/.*flwr\[simulation\].*//' pyproject.toml \
    && python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir \
       --index-url https://download.pytorch.org/whl/cu128 \
       --extra-index-url https://pypi.org/simple \
       torch \
    && python -m pip install --no-cache-dir .

ENTRYPOINT ["flower-superexec"]