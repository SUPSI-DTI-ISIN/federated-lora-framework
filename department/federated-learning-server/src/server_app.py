from f__all__lwr.app import ArrayRecord, ConfigRecord, Context
from flwr.serverapp import Grid, ServerApp
from flwr.serverapp.strategy import FedAvg
from peft import get_peft_model_state_dict

from commons.services.model import ModelService
from commons.utils import settings

app = ServerApp()

@app.main()
def main(grid: Grid, context: Context) -> None:
    model_name: str = context.run_config["model-name"]
    fraction_train: float = context.run_config["fraction-train"]
    num_rounds: int = context.run_config["num-server-rounds"]
    lr: float = context.run_config["lr"]
    device: str = context.run_config["device"]

    global_model = ModelService.load_model(model_name=model_name, device=device, lora_config=settings.lora_config)
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

    #os.makedirs(os.path.normpath("./output"), exist_ok=True)
    #torch.save(state_dict, "final_model.pt")