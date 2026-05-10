# Institute Service

Manages the registry of institutes participating in the federation. Provides CRUD operations for institute records and exposes the institute list to the frontend and other department services.

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
DATABASE_URL="mysql+aiomysql://root:root@localhost:33062/institutes"
ALEMBIC_SYNC_DATABASE_URL="mysql+pymysql://root:root@localhost:33062/institutes"
FRONTEND_URL="http://localhost:3000"
REALM_NAME="Department"
DEPARTMENT_URL="http://localhost:80"
KEYCLOAK_URL="http://localhost:8086"
```

> Make sure the department infrastructure is running via `docker compose -f docker-compose.local.yml` before starting this service.

### 4. Run database migrations

```bash
uv run --env-file .env.dev alembic upgrade head
```

### 5. Start the service

```bash
uv run --env-file .env.dev src/institute_service.py
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
