import os

import torch
from flwr.app import ArrayRecord, Context, Message, MetricRecord, RecordDict
from flwr.clientapp import ClientApp
from peft import set_peft_model_state_dict

from app.config.settings import settings
from app.dataset import dataset_builder
from app.parser import parse_pdf_files
from app.training.core import load_peft_model, load_data

# Flower ClientApp
app = ClientApp()

"""
_MODEL = None
_TOKENIZER = None
_DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
_DATASET_FILE = None

@app.lifespan()
def lifespan(context: Context):
    global _MODEL, _TOKENIZER, _DATASET_FILE

    model_name: str = context.run_config["model-name"]
    pdf_folder: str = context.run_config["pdf-folder"]
    node_id: int = context.node_id


    _MODEL, _TOKENIZER = load_peft_model(model_name)
    _MODEL.to(_DEVICE)
    _MODEL.eval()

    documents = parse_pdf_files(pdf_folder)
    dataset = dataset_builder.build_dataset_from_documents(documents)
    file_name = "dataset" + str(node_id) + ".jsonl"
    _DATASET_FILE = os.path.join(settings.output_folder, file_name)
    os.makedirs(os.path.dirname(_DATASET_FILE), exist_ok=True)
    dataset.to_jsonl(_DATASET_FILE)

    yield

    _MODEL = None
    _TOKENIZER = None
"""

@app.train()
def train(msg: Message, context: Context):
    """Train the model on local data."""
    print("Client App called")
    """global _MODEL, _TOKENIZER, _DATASET_FILE

    model_name = context.node_config["model-name"]
    node_id: int = context.node_id

    if _MODEL is None:
        _MODEL, _TOKENIZER = load_peft_model(model_name)
        _MODEL.to(_DEVICE)

    if _DATASET_FILE is None:
        file_name = "dataset" + str(node_id) + ".jsonl"
        _DATASET_FILE = os.path.join(settings.output_folder, file_name)

    peft_state = msg.content["arrays"].to_torch_state_dict()
    set_peft_model_state_dict(_MODEL, peft_state)
    _MODEL.train()

    train_dataset, eval_dataset = load_data(_DATASET_FILE)

    # Load the data
    
    train_loss, train_acc = train_fn()
    trainloader, _ = load_data(partition_id, num_partitions)

    # Call the training function
    train_loss = train_fn(
        model,
        trainloader,
        context.run_config["local-epochs"],
        msg.content["config"]["lr"],
        device,
    )

    # Construct and return reply Message
    model_record = ArrayRecord(model.state_dict())
    metrics = {
        "train_loss": train_loss,
        "num-examples": len(trainloader.dataset),
    }
    metric_record = MetricRecord(metrics)
    content = RecordDict({"arrays": model_record, "metrics": metric_record})
    return Message(content=content, reply_to=msg)
    """
    return Message(content=RecordDict(), reply_to=msg)

@app.evaluate()
def evaluate(msg: Message, context: Context):
    """Evaluate the model on local data."""

    # Load the model and initialize it with the received weights
    """
    model = Net()
    model.load_state_dict(msg.content["arrays"].to_torch_state_dict())
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Load the data
    partition_id = context.node_config["partition-id"]
    num_partitions = context.node_config["num-partitions"]
    _, valloader = load_data(partition_id, num_partitions)

    # Call the evaluation function
    eval_loss, eval_acc = test_fn(
        model,
        valloader,
        device,
    )

    # Construct and return reply Message
    metrics = {
        "eval_loss": eval_loss,
        "eval_acc": eval_acc,
        "num-examples": len(valloader.dataset),
    }
    metric_record = MetricRecord(metrics)
    content = RecordDict({"metrics": metric_record})
    return Message(content=content, reply_to=msg)
    """
    return Message(content=RecordDict(), reply_to=msg)