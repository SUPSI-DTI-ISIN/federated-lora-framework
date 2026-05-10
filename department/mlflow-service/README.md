# MLflow Service

FastAPI wrapper around MLflow that exposes experiment tracking and model registry capabilities to the rest of the department stack. Handles model artifact storage, run logging, and serves fine-tuned model weights to institute nodes via the Model Service.

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

> **Docker builds:** revert this change (comment the path, uncomment the `index = "gitlab"` line) before building a Docker image.

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
MODEL_BASE_PATH="../../models/department"
REALM_NAME="Department"
KEYCLOAK_URL="http://localhost:8086"
FRONTEND_URL="http://localhost:3000"
DEVICE_MAP="auto"
```

> Make sure the department infrastructure (Keycloak, databases, Redis) is running via `docker compose -f docker-compose.local.yml` before starting this service.

### 4. Start the service

```bash
uv run --env-file .env.dev src/mlflow_service.py
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
