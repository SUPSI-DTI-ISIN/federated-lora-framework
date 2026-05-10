# Inference Service

Runs LLM inference using the locally stored model (base or fine-tuned). Inference requests are queued via Celery/Redis so the GPU is never overloaded. Supports 4-bit quantization via BitsAndBytes and LoRA adapter loading via PEFT.

## Local Development

### 1. Switch to the local shared-auth-library

Open `pyproject.toml` and toggle the `[tool.uv.sources]` block so the library is resolved from your local path instead of the GitLab registry:

```toml
[tool.uv.sources]
# For local development — use the local path:
shared-auth-library = { path = "../../shared-auth-library" }
# For Docker builds — use the GitLab registry (comment the line above, uncomment below):
# shared-auth-library = { index = "gitlab" }
```

> **Docker builds:** revert this change before building a Docker image.

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure the environment

```bash
cp .env.dev.template .env.dev
```

The template already contains sensible defaults for local development:

```dotenv
MAX_CACHED_MODELS=1
DEVICE_MAP="auto"
FRONTEND_URL="http://localhost:3000"
MODEL_SERVICE_URL="http://localhost:8090"
INSTITUTE_NAME="ISIN"
KEYCLOAK_URL="http://localhost:8086"
REDIS_URL="redis://localhost:6380"
```

> Make sure the institute infrastructure is running via `docker compose -f docker-compose.local.yml` and the Model Service is reachable before starting this service.

### 4. Start the API server

```bash
uv run --env-file .env.dev src/inference_service.py
```

### 5. Start the Celery worker (separate terminal)

```bash
PYTHONPATH=src uv run --env-file .env.dev celery -A src.clients.celery worker --loglevel=info
```

---

## Running Tests

```bash
uv run pytest
```

---

## Docker

> Ensure `pyproject.toml` uses `shared-auth-library = { index = "gitlab" }` before building.

← [Back to root README](../../README.md)
