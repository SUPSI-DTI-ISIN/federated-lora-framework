FROM --platform=$TARGETPLATFORM flwr/superexec:1.25.0

USER root
RUN apt-get update \
    && apt-get -y --no-install-recommends install \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

#USER app

WORKDIR /app
COPY pyproject.toml .
RUN sed -i 's/.*flwr\[simulation\].*//' pyproject.toml \
    && python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir \
       --index-url https://download.pytorch.org/whl/cu128 \
       --extra-index-url https://pypi.org/simple \
       torch \
    && python -m pip install --no-cache-dir .

ENTRYPOINT ["flower-superexec"]

#FROM --platform=$TARGETPLATFORM flwr/superexec:1.25.0
#
#USER root
#
#RUN apt-get update && apt-get install -y --no-install-recommends curl
#
#USER app
#
#RUN curl -LsSf https://astral.sh/uv/install.sh | sh
#ENV PATH="/home/app/.local/bin:$PATH"
#
#WORKDIR /app
#COPY pyproject.toml .
#COPY uv.lock .
#RUN sed -i 's/.*flwr\[simulation\].*//' pyproject.toml
#
#RUN uv sync --no-dev --locked
#
#ENTRYPOINT ["flower-superexec"]