# Federated Learning Service

Contains the Flower **ServerApp** and **ClientApp** that implement the federated fine-tuning logic. The ServerApp runs on the department node (via SuperLink), the ClientApp runs on each institute node (via SuperNode). Both use PEFT/LoRA to fine-tune Llama-2-7b-chat-hf with minimal GPU memory.


## Architecture

```
Department node                    Institute nodes
┌─────────────────┐               ┌──────────────────┐
│  SuperLink      │◄─────────────►│  SuperNode       │
│  (9091-9093)    │               │  (9094)          │
│                 │               │                  │
│  ServerApp      │               │  ClientApp       │
│  (aggregation)  │               │  (local training)│
└─────────────────┘               └──────────────────┘
```

The ServerApp aggregates model updates using FedAvg. The ClientApp loads the local dataset from the institute's Data Service, fine-tunes for a configurable number of local epochs, and returns only the LoRA adapter weights.

---

## Configuration

Key parameters in `pyproject.toml` under `[tool.flwr.app.config]`:

| Parameter           | Default | Description                            |
|---------------------|---------|----------------------------------------|
| `num-server-rounds` | 2       | Number of federation rounds            |
| `fraction-train`    | 0.5     | Fraction of clients selected per round |
| `local-epochs`      | 1       | Local training epochs per round        |
| `lr`                | 0.01    | Learning rate                          |

---

## Local Simulation

Run a local simulation with 2 virtual supernodes (no real network):

```bash
uv sync
source .venv/bin/activate
cd scripts
./run_simulation.sh
```

---

## Running Tests

```bash
uv run pytest
```

---

## Deployment

The ClientApp and ServerApp are packaged as a Flower FAB and deployed via the SuperExec container. See the department and institute Docker Compose files for the full deployment setup.

← [Back to root README](../README.md)
