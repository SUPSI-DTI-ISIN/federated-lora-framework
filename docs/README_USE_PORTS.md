# Port Usage Registry

This document tracks all **host-exposed ports** used by the current Docker Compose setup.
Check this file before assigning ports to new services.

---

## Department Stack

| Port | Service                  | Purpose / Notes                 |
|------|--------------------------|---------------------------------|
| 5432 | PostgreSQL               | MLflow backend database         |
| 9000 | MinIO API                | S3-compatible artifact storage  |
| 9001 | MinIO Console            | MinIO web UI                    |
| 5000 | MLflow Server            | MLflow tracking server          |
| 9010 | MLflow Service API       | Department MLflow API           |
| 81   | Department NGINX Gateway | Reverse proxy to MLflow service |
| 8085 | Keycloak                 | Authentication Service          |

---

## Institute Stack

| Port | Service           | Purpose / Notes              |
|------|-------------------|------------------------------|
| 3306 | MySQL             | Institute main database      |
| 8095 | Inference Service | Model inference API          |
| 8080 | Data Service      | Data access & management API |
| 8081 | Chat Service      | Chat handler API             |
| 8090 | Model Service     | Model orchestration API      |
| 80   | Frontend          | Web UI                       |