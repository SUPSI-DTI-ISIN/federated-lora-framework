import os

from flwr.app import ArrayRecord, ConfigRecord, Context
from flwr.serverapp import Grid, ServerApp
from flwr.serverapp.strategy import FedAvg
from peft import get_peft_model_state_dict, set_peft_model_state_dict
from transformers import PreTrainedModel

from src.federated_learning_server.clients.mlflow import MlFlowServiceClientInterface, MlFlowServiceClient
from src.federated_learning_server.config import settings
from src.federated_learning_common.services.model import ModelService

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

    pretrained_global_model: PreTrainedModel = ModelService.load_model(model_path=federated_data_dto.model_path, device_map=settings.device_map)

    if federated_data_dto.latest_adapter_path is None:
        print("No previous adapter found. Initialising fresh LoRA adapter")
        peft_model = ModelService.get_peft_model(model=pretrained_global_model)
    else:
        print(f"Resuming from existing adapter: {federated_data_dto.latest_adapter_path}")
        peft_model = ModelService.load_peft_model(
             model=pretrained_global_model,
            adapter_path=federated_data_dto.latest_adapter_path
        )

    del pretrained_global_model

    ModelService.print_trainable_parameters(model=peft_model)
    peft_state = get_peft_model_state_dict(peft_model)

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

    set_peft_model_state_dict(peft_model, state_dict)

    os.makedirs(federated_data_dto.new_adapter_path, exist_ok=True)
    peft_model.save_pretrained(federated_data_dto.new_adapter_path)

    print(f"Adapter saved correctly to: {federated_data_dto.new_adapter_path}")