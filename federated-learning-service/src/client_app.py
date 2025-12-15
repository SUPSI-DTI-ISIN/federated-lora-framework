import os

from flwr.app import Context, Message, RecordDict
from flwr.clientapp import ClientApp
from flwr.common import ArrayRecord, MetricRecord
from peft import set_peft_model_state_dict, get_peft_model_state_dict

from config import settings
from dataset.dataset_builder import build_dataset_from_documents
from model_service import ModelService
from parser import parse_pdf_files
from training.core import load_data, train_local

app = ClientApp()

@app.lifespan()
def lifespan(context: Context):
    print("Entro nel lifespan...")
    model_name: str = context.run_config["model-name"]
    pdf_folder: str = context.run_config["pdf-folder"]

    model_service = ModelService.get_model_service(model_name=model_name)

    documents = parse_pdf_files(pdf_folder=pdf_folder)
    dataset = build_dataset_from_documents(documents=documents)

    os.makedirs(os.path.dirname(settings.dataset_path), exist_ok=True)
    dataset.to_jsonl(output_path=settings.dataset_path)

    yield

    del model_service
    print("Esco dal lifespan...")

@app.train()
def train(msg: Message, context: Context):
    print("Client App called")

    model_name: str = context.run_config["model-name"]

    model_service = ModelService.get_model_service(model_name=model_name)

    peft_state = msg.content["arrays"].to_torch_state_dict()
    llm_model = model_service.llm_model
    set_peft_model_state_dict(llm_model.model, peft_state)
    llm_model.model.train()

    train_dataset, eval_dataset = load_data(dataset_path=settings.dataset_path)

    train_metrics = train_local(
        model=llm_model.model,
        tokenizer=llm_model.tokenizer,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset
    )

    print(f"Train metrics: {train_metrics}")

    peft_state_out = get_peft_model_state_dict(llm_model.model)
    arrays = ArrayRecord(peft_state_out)

    metrics = {
        "train_loss": train_metrics.get("train_loss", None),
        "eval_loss": train_metrics.get("eval_loss", None),
        "num-examples": int(len(train_dataset)),
    }
    metric_record = MetricRecord(metrics)

    content = RecordDict({"arrays": arrays, "metrics": metric_record})
    return Message(content=content, reply_to=msg)


@app.evaluate()
def evaluate(msg: Message, context: Context):
    """Evaluate the model on local data."""

    print("Start evaluation...")

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