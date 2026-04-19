from flwr.app import ArrayRecord, ConfigRecord, Context
from flwr.serverapp import Grid, ServerApp
from flwr.serverapp.strategy import FedAvg

from src.federated_learning_server.clients.mlflow import MlFlowServiceClientInterface, MlFlowServiceClient
from src.federated_learning_server.config import settings
from src.federated_learning_server.services import AdapterService

app = ServerApp()

@app.main()
def main(grid: Grid, context: Context) -> None:
    mlflow_service_client: MlFlowServiceClientInterface = MlFlowServiceClient.get_instance(mlflow_service_url=settings.mlflow_service_url)
    federated_data_dto = mlflow_service_client.get_federated_data(model_key=settings.model_key)
    print(federated_data_dto)
    print(f"Node ids {grid.get_node_ids()}")
    print(f"Server node id {context.node_id}")

    fraction_train: float = context.run_config.get("fraction-train", 0.5)
    num_rounds: int = context.run_config.get("num-server-rounds", 3)
    lr: float = context.run_config.get("lr", 0.01)

    print(f"Get latest adapter: {federated_data_dto.latest_adapter_path}")

    peft_state = AdapterService.load_adapter_state_dict(adapter_path=federated_data_dto.latest_adapter_path)

    arrays = ArrayRecord(peft_state)

    strategy = FedAvg(
        fraction_train=fraction_train,
    )

    result = strategy.start(
        grid=grid,
        initial_arrays=arrays,
        train_config=ConfigRecord({"lr": lr}),
        num_rounds=num_rounds,
        timeout=7200
    )

    print("\nSaving final model to disk...")
    state_dict = result.arrays.to_torch_state_dict()

    AdapterService.save_adapter(state_dict=state_dict, new_adapter_path=federated_data_dto.new_adapter_path, source_adapter_path=federated_data_dto.latest_adapter_path)

    print(f"Adapter saved correctly to: {federated_data_dto.new_adapter_path}")