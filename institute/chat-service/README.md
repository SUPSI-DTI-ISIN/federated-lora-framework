# Chat Service

Handles chat sessions between users and the LLM. Persists conversation history in MySQL, forwards inference requests to the Inference Service, and streams responses back to the frontend via Server-Sent Events (SSE).

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
INFERENCE_SERVICE_URL="http://localhost:8095"
INSTITUTE_NAME="ISIN"
KEYCLOAK_URL="http://localhost:8086"
DATABASE_URL="mysql+aiomysql://root:root@localhost:33061/chats"
ALEMBIC_SYNC_DATABASE_URL="mysql+pymysql://root:root@localhost:33061/chats"
FRONTEND_URL="http://localhost:3000"
REDIS_URL="redis://localhost:6380"
```

> Make sure the institute infrastructure is running via `docker compose -f docker-compose.local.yml` and the Inference Service is reachable before starting this service.

### 4. Run database migrations

```bash
uv run --env-file .env.dev alembic upgrade head
```

### 5. Start the service

```bash
uv run --env-file .env.dev src/chat_service.py
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
