#!/usr/bin/env bash
set -e

wait_for_db() {
  host="${DB_HOST}"
  port="${DB_PORT}"
  max_attempts=30
  attempt=1

  echo "Waiting for database $host:$port ..."
  while ! nc -z "$host" "$port"; do
    attempt=$((attempt+1))
    if [ "$attempt" -gt "$max_attempts" ]; then
      echo "Timed out waiting for DB at $host:$port"
      return 1
    fi
    sleep 1
  done
  echo "Database is reachable."
}


if [ -z "${ALEMBIC_SYNC_DATABASE_URL:-}" ]; then
  echo "ALEMBIC_SYNC_DATABASE_URL is not unset; aborting."
  exit 1
else
  echo "Using ALEMBIC_SYNC_DATABASE_URL from environment."
fi

echo "Using DB host: ${DB_HOST}:${DB_PORT}"

wait_for_db

echo "Running alembic migrations (using ALEMBIC_SYNC_DATABASE_URL)..."
for i in 1 2 3; do
  if uv run alembic upgrade head; then
    echo "Migrations applied."
    break
  else
    echo "Migration attempt $i failed. Retrying in 1s"
    sleep 1
  fi
done

echo "Starting application..."
uv run src/chat_service.py -p 8081