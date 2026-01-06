FROM flwr/superexec:1.23.0

WORKDIR /app

COPY pyproject.toml .
COPY pdf-innosuisse ./pdf-innosuisse
RUN pip install --upgrade pip
RUN python -m pip install -U --no-cache-dir .

ENTRYPOINT ["flower-superexec"]