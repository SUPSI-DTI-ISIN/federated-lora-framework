# Model Service

Manages the lifecycle of model weights on the institute node. Fetches fine-tuned adapter weights from the department's MLflow Service, stores them locally, and exposes the active model path to the Inference Service and the federated learning ClientApp.

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
MODEL_KEY="llama-2-7b"
MODEL_BASE_PATH="../../models/institute/ISIN"
FRONTEND_URL="http://localhost:3000"
MLFLOW_DEPARTMENT_SERVICE_URL="http://localhost:9010/api_mlflow"
INSTITUTE_NAME="ISIN"
KEYCLOAK_URL="http://localhost:8086"
```

> Make sure the institute infrastructure is running via `docker compose -f docker-compose.local.yml` and the department MLflow Service is reachable before starting this service.

### 4. Start the service

```bash
uv run --env-file .env.dev src/model_service.py
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
