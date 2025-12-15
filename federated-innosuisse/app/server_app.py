import os
import torch

from flwr.app import ArrayRecord, ConfigRecord, Context
from flwr.serverapp import Grid, ServerApp
from flwr.serverapp.strategy import FedAvg
from peft import get_peft_model_state_dict

from app.model_service import ModelService
from app.training.core import print_trainable_parameters

app = ServerApp()

@app.main()
def main(grid: Grid, context: Context) -> None:
    model_name: str = context.run_config["model-name"]
    fraction_train: float = context.run_config["fraction-train"]
    num_rounds: int = context.run_config["num-server-rounds"]
    lr: float = context.run_config["lr"]

    model_service = ModelService.get_model_service(model_name=model_name)

    global_model = model_service.llm_model.model
    print_trainable_parameters(global_model)
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

    #os.makedirs(os.path.normpath("./output"), exist_ok=True)
    #torch.save(state_dict, "final_model.pt")