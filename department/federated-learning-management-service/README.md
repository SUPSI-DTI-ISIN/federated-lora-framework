# Federated Learning Management Service

Orchestrates federated learning jobs across registered institutes. Accepts job requests from the frontend, dispatches them to Celery workers, monitors job status via Server-Sent Events (SSE), and communicates with the Flower SuperLink to trigger federation rounds.

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
DATABASE_URL="mysql+aiomysql://root:root@localhost:33063/federated_learning_jobs"
ALEMBIC_SYNC_DATABASE_URL="mysql+pymysql://root:root@localhost:33063/federated_learning_jobs"
REALM_NAME="Department"
KEYCLOAK_URL="http://localhost:8086"
FRONTEND_URL="http://localhost:3000"
REDIS_URL="redis://localhost:6379"
FLWR_APP_BASE_PATH="../../federated-learning-service"
IS_FEDERATED_LEARNING_SIMULATION_ENVIRONMENT=True
```

> Make sure the department infrastructure is running via `docker compose -f docker-compose.local.yml` before starting this service.

### 4. Run database migrations

```bash
uv run --env-file .env.dev alembic upgrade head
```

### 5. Start the API server

```bash
uv run --env-file .env.dev src/federated_learning_management_service.py
```

### 6. Start the Celery worker (separate terminal)

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

### Prepare the Flower FAB

Before starting the containers, the federated learning app must be built and installed into the `flwr/` directory. The Celery worker uses it to launch FL fine-tuning jobs via the Flower CLI.

**Step 1 — build the FAB**

```bash
cd federated-learning-service
uv sync
flwr build
```

This produces `luca-fanto.federated-learning-service.<version>.fab` in the current directory.

**Step 2 — copy the FAB**

```bash
cp luca-fanto.federated-learning-service.*.fab \
   ../department/federated-learning-management-service/flwr/fab/
```

**Step 3 — install the FAB**

```bash
cd ../department/federated-learning-management-service/flwr
flwr install fab/luca-fanto.federated-learning-service.<version>.fab --flwr-dir .
```

This creates the app under `./apps/luca-fanto.federated-learning-service.<version>/`. Check the exact name with `ls apps/`.

**Step 4 — copy the pyproject.toml into the installed app**

```bash
cp ../../../federated-learning-service/pyproject.toml \
   apps/luca-fanto.federated-learning-service.<version>/pyproject.toml
```

> Repeat steps 1–4 whenever `federated-learning-service` is updated.

### Start the containers

Three containers are started from the same image:

```bash
docker compose -f ../../docker/docker-compose.department.yml --env-file ../docker/.env up -d \
  federated-learning-management-service \
  federated-learning-management-service-worker \
  federated-learning-management-service-flower
```

← [Back to root README](../../README.md)
