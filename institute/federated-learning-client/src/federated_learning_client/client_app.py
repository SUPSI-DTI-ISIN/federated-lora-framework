from flwr.app import Context, Message, RecordDict
from flwr.clientapp import ClientApp
from flwr.common import ArrayRecord, MetricRecord
from peft import set_peft_model_state_dict, get_peft_model_state_dict

from federated_learning_client.config import settings
from federated_learning_client.clients.data_service import DataServiceClientInterface, DataServiceClient
from federated_learning_client.clients.model_service import ModelServiceClientInterface, ModelServiceClient
from federated_learning_client.services.dataset import DatasetService
from federated_learning_client.services.training import TrainingService

from federated_learning_common.services.model import ModelService

app = ClientApp()

@app.lifespan()
def lifespan(context: Context):
    print("Enter lifespan...")

    #data_service_url: str = context.run_config["data-service-url"]
    data_service_url = settings.data_service_url

    document_service: DataServiceClientInterface = DataServiceClient.get_instance(data_service_url=data_service_url)
    documents = document_service.get_documents()

    training_dataset = DatasetService.build_dataset_from_documents(documents=documents)
    DatasetService.save_dataset_to_jsonl(training_dataset=training_dataset)

    yield

    print("Exit lifespan...")

@app.train()
def train(msg: Message, context: Context):
    print("Client App called")
    model_key = settings.model_key
    device_map = settings.device_map
    model_service_url = settings.model_service_url

    model_service_client: ModelServiceClientInterface = ModelServiceClient.get_instance(model_service_url=model_service_url)
    model_path_dto = model_service_client.get_model_path(model_key=model_key)

    peft_state = msg.content["arrays"].to_torch_state_dict()
    model = ModelService.load_model(model_path=model_path_dto.model_base_path, device_map=device_map, access_token=settings.hf_token)
    tokenizer = ModelService.load_tokenizer(model_path=model_path_dto.model_base_path, access_token=settings.hf_token)

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

    peft_state_out = get_peft_model_state_dict(model)
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