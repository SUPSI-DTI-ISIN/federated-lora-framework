# Frontend

React + TypeScript single-page application that serves as the unified UI for both department operators and institute users. Communicates with backend services through auto-generated TypeScript clients.

## Local Development

### Prerequisites

Before starting the frontend, all backend services must be running and the API clients must be synced. If you haven't done this yet, go back to the [root README](../../README.md) and follow the development guide.

### 1. Configure the environment

```bash
cp .env.development.template .env.development
```

The template already contains sensible defaults that match the dev ports of all services:

```dotenv
VITE_FEDERATED_LEARNING_MANAGEMENT_SERVICE_URL=http://localhost:9015
VITE_INSTITUTE_SERVICE_URL=http://localhost:9020
VITE_MLFLOW_SERVICE_URL=http://localhost:9010
VITE_CHAT_SERVICE_URL=http://localhost:8081
VITE_DATA_SERVICE_URL=http://localhost:8080
VITE_MODEL_SERVICE_URL=http://localhost:8090
VITE_MODEL_KEY=llama-2-7b
VITE_ENVIRONMENT=development
VITE_KEYCLOAK_URL=http://localhost:8086
VITE_FRONTEND_URL=http://localhost:3000
VITE_FLOWER_CELERY_JOBS_URL=http://localhost:5555
VITE_CLIENT_ID=spa-client
```

### 2. Install dependencies

```bash
npm install
```

### 3. Start the dev server

```bash
npm run dev
```

The app is available at `http://localhost:3000`.

---

## Running Tests

```bash
npm run test
```

Generate a coverage report:

```bash
npm run test:coverage
```

---

## Build

```bash
npm run build
```

Output is in `dist/`.

← [Back to root README](../README.md)
