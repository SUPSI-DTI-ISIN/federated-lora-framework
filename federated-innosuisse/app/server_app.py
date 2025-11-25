import torch
from flwr.app import ArrayRecord, ConfigRecord, Context
from flwr.serverapp import Grid, ServerApp
from flwr.serverapp.strategy import FedAvg
from peft import get_peft_model_state_dict

from app.training.core import load_peft_model, print_trainable_parameters

# Create ServerApp
app = ServerApp()


@app.main()
def main(grid: Grid, context: Context) -> None:
    """Main entry point for the ServerApp."""

    # Read run config
    model_name: str = context.run_config["model-name"]
    fraction_train: float = context.run_config["fraction-train"]
    num_rounds: int = context.run_config["num-server-rounds"]
    lr: float = context.run_config["lr"]

    print(f"Model name: {model_name}")
    print(f"Fraction train: {fraction_train}")
    print(f"Number of rounds: {num_rounds}")
    print(f"LR: {lr}")

    # Load global model
    #global_model, _ = load_peft_model(model_name)
    #print_trainable_parameters(global_model)

    #peft_state = get_peft_model_state_dict(global_model)
    #arrays = ArrayRecord(peft_state)
    arrays = ArrayRecord()

    # Initialize FedAvg strategy
    strategy = FedAvg(fraction_train=fraction_train)

    # Start strategy, run FedAvg for `num_rounds`
    result = strategy.start(
        grid=grid,
        initial_arrays=arrays,
        train_config=ConfigRecord({"lr": lr}),
        num_rounds=num_rounds,
    )

    # Save final model to disk
    print("\nSaving final model to disk...")
    #state_dict = result.arrays.to_torch_state_dict()
    #torch.save(state_dict, "final_model.pt")