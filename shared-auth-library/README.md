# Shared Auth Library

A shared Python library that provides JWT/OIDC token validation and FastAPI dependency injection helpers. Used by all Python microservices in both the department and institute stacks to avoid duplicating authentication logic.

Published to the internal GitLab PyPI registry and consumed by services via `uv`.


## Local Development

```bash
uv sync
```

Build the library (required before other services can install it from a local path):

```bash
uv build
```

---

## Using in Other Services

### Local development (path reference)

In each service's `pyproject.toml`, comment out the GitLab index source and uncomment the local path:

```toml
[tool.uv.sources]
# For local development:
shared-auth-library = { path = "../../shared-auth-library" }
# For Docker builds (comment the line above, uncomment below):
# shared-auth-library = { index = "gitlab" }
```

Then run `uv sync` in the service directory.

### Docker builds (registry reference)

Revert to the GitLab index before building any Docker image:

```toml
[tool.uv.sources]
# shared-auth-library = { path = "../../shared-auth-library" }
shared-auth-library = { index = "gitlab" }
```

---

## Running Tests

```bash
uv run pytest
```

---

## Publishing

Build and publish to the GitLab registry:

```bash
cd scrpts
./build-and-push.sh
```

Configure your GitLab credentials in `.pypirc` (copy from `.pypirc.template`).

← [Back to root README](../README.md)
