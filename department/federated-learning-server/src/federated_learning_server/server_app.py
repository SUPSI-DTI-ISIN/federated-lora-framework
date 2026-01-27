import os
import torch

from flwr.app import ArrayRecord, ConfigRecord, Context
from flwr.serverapp import Grid, ServerApp
from flwr.serverapp.strategy import FedAvg
from peft import get_peft_model_state_dict

from federated_learning_server.clients.mlflow import MlFlowServiceClientInterface, MlFlowServiceClient
from federated_learning_server.config import settings
from federated_learning_common.services.model import ModelService

app = ServerApp()

@app.main()
def main(grid: Grid, context: Context) -> None:
    mlflow_service_client: MlFlowServiceClientInterface = MlFlowServiceClient.get_instance(mlflow_service_url=settings.mlflow_service_url)
    federated_data_dto = mlflow_service_client.get_federated_data(model_key=settings.model_key)
    print(federated_data_dto)

    device_map: str = settings.device_map
    fraction_train: float = context.run_config["fraction-train"]
    num_rounds: int = context.run_config["num-server-rounds"]
    lr: float = context.run_config["lr"]

    global_model = ModelService.load_model(model_path=federated_data_dto.model_path, device_map=device_map, access_token=settings.hf_token)
    ModelService.print_trainable_parameters(model=global_model)
    peft_state = get_peft_model_state_dict(global_model)

    arrays = ArrayRecord(peft_state)

    strategy = FedAvg(fraction_train=fraction_train)

    result = strategy.start(
        grid=grid,
        initial_arrays=arrays,
        train_config=ConfigRecord({"lr": lr}),
        num_rounds=num_rounds,
    )

    print("\nSaving final model to disk...")
    state_dict = result.arrays.to_torch_state_dict()

    os.makedirs(federated_data_dto.new_adapter_path, exist_ok=True)
    torch.save(state_dict, "final_model.pt")