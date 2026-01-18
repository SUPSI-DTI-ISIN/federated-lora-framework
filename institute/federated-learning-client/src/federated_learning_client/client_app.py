from typing import List

from flwr.app import Context, Message, RecordDict
from flwr.clientapp import ClientApp
from flwr.common import ArrayRecord, MetricRecord
from peft import set_peft_model_state_dict, get_peft_model_state_dict

from domain.document import DocumentDTO
from domain.training import TrainingDataset
from services.dataset import DatasetService
from services.document import DocumentService
from services.training import TrainingService

from federated_learning_common.config import settings as commons_settings
from federated_learning_common.services.model import ModelService

app = ClientApp()

@app.lifespan()
def lifespan(context: Context):
    print("Enter lifespan...")

    data_service_url: str = context.run_config["data-service-url"]

    document_service: DocumentService = DocumentService.get_instance(data_service_url=data_service_url)
    documents: List[DocumentDTO] = document_service.get_documents()

    training_dataset: TrainingDataset = DatasetService.build_dataset_from_documents(documents=documents)
    DatasetService.save_dataset_to_jsonl(training_dataset=training_dataset)

    yield

    print("Exit lifespan...")

@app.train()
def train(msg: Message, context: Context):
    print("Client App called")
    model_name: str = context.run_config["model-name"]
    device: str = context.run_config["device"]

    peft_state = msg.content["arrays"].to_torch_state_dict()
    model = ModelService.load_model(model_name=model_name, device=device, lora_config=commons_settings.lora_config)
    tokenizer = ModelService.load_tokenizer(model_name=model_name)
    set_peft_model_state_dict(model, peft_state)
    model.train()

    train_dataset, eval_dataset = DatasetService.load_data()

    train_metrics = TrainingService.train(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset
    )

    print(f"Train metrics: {train_metrics}")

    peft_state_out = get_peft_model_state_dict(model.model)
    arrays = ArrayRecord(peft_state_out)

    metrics = {
        "train_loss": train_metrics.get("train_loss", None),
        "eval_loss": train_metrics.get("eval_loss", None),
        "num-examples": int(len(train_dataset)),
    }
    metric_record = MetricRecord(metrics)

    content = RecordDict({"arrays": arrays, "metrics": metric_record})
    return Message(content=RecordDict(), reply_to=msg)


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