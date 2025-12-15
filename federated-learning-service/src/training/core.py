import os.path
import torch
import torch.nn as nn

from datasets import load_dataset, Split
from peft import LoraConfig, get_peft_model
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, \
    IntervalStrategy, DataCollatorForLanguageModeling

from config import settings
from domain.llm_model import LlmModel

LORA_CONFIG = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.05,
    bias='none',
    task_type="CAUSAL_LM",
)

def print_trainable_parameters(model):
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()

    print(f"Trainable parameters: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param:.2f}%")


def load_peft_model(model_name: str) -> LlmModel:
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto"
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token

    for param in model.parameters():
        param.requires_grad = False
        if param.ndim == 1:
            param.data = param.data.to(torch.float32)

    model.gradient_checkpointing_disable()
    model.enable_input_require_grads()

    class CastOutputToFloat(nn.Sequential):
        def forward(self, x): return super().forward(x).to(torch.float32)

    model.lm_head = CastOutputToFloat(model.lm_head)

    model = get_peft_model(model, LORA_CONFIG)

    llm_model = LlmModel(model=model, tokenizer=tokenizer)

    return llm_model


def load_data(dataset_path: str, test_size: float = 0.25):
    dataset = load_dataset("json", data_files={"train": dataset_path}, split=Split.TRAIN)

    dataset = dataset.train_test_split(test_size=test_size)
    train_dataset = dataset['train']
    eval_dataset = dataset['test']

    return train_dataset, eval_dataset


def train_local(model, tokenizer, train_dataset, eval_dataset):
    def preprocess(examples):
        prompts = []
        for i in range(len(examples['instruction'])):
            prompt = f"{examples['instruction'][i]}\n\nInput:\n{examples['input'][i]}\n\nOutput:\n"
            full_text = prompt + examples['output'][i]
            prompts.append(full_text)

        tokenized = tokenizer(
            prompts,
            max_length=512,
            truncation=True,
            padding=False,
        )

        tokenized["labels"] = [ids.copy() for ids in tokenized["input_ids"]]

        return tokenized

    train_dataset = train_dataset.map(
        preprocess,
        batched=True,
        remove_columns=train_dataset.column_names,
    )
    eval_dataset = eval_dataset.map(
        preprocess,
        batched=True,
        remove_columns=eval_dataset.column_names,
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer,
        mlm=False
    )

    training_folder = os.path.join(settings.output_folder, "training")
    adapter_folder = os.path.join(settings.output_folder, "adapter")
    os.makedirs(training_folder, exist_ok=True)
    os.makedirs(adapter_folder, exist_ok=True)

    training_args = TrainingArguments(
        output_dir=training_folder,

        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=8,

        num_train_epochs=2,
        max_steps=200,

        learning_rate=2e-4,
        warmup_steps=100,

        fp16=False,
        bf16=False,

        eval_strategy=IntervalStrategy.EPOCH,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator
    )

    model.config.use_cache=False
    train_output = trainer.train()
    eval_metrics = trainer.evaluate()

    metrics = {
        "train_loss": float(train_output.training_loss) if hasattr(train_output, "training_loss") else None,
        "eval_loss": eval_metrics.get("eval_loss"),
        "hf_train_metrics": train_output.metrics if hasattr(train_output, "metrics") else None,
    }
    return metrics





def train(dataset_file: str):
    model = AutoModelForCausalLM.from_pretrained(
        'distilbert/distilgpt2',
        device_map="auto",
    )

    tokenizer = AutoTokenizer.from_pretrained('distilbert/distilgpt2')
    tokenizer.pad_token = tokenizer.eos_token

    for param in model.parameters():
        param.requires_grad = False
        if param.ndim == 1:
            param.data = param.data.to(torch.float32)

    model.gradient_checkpointing_disable()
    model.enable_input_require_grads()

    class CastOutputToFloat(nn.Sequential):
        def forward(self, x): return super().forward(x).to(torch.float32)

    model.lm_head = CastOutputToFloat(model.lm_head)

    config = LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.05,
        bias='none',
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(model, config)
    print_trainable_parameters(model)

    dataset = load_dataset("json", data_files={"train": dataset_file}, split="train")

    dataset = dataset.train_test_split(test_size=0.25)
    train_dataset = dataset['train']
    eval_dataset = dataset['test']

    print(f"Dataset: {len(train_dataset)} training, {len(eval_dataset)} validation")

    def preprocess(examples):
        prompts = []
        for i in range(len(examples['instruction'])):
            prompt = f"{examples['instruction'][i]}\n\nInput:\n{examples['input'][i]}\n\nOutput:\n"
            full_text = prompt + examples['output'][i]
            prompts.append(full_text)

        tokenized = tokenizer(
            prompts,
            max_length=512,
            truncation=True,
            padding=False,
        )

        tokenized["labels"] = [ids.copy() for ids in tokenized["input_ids"]]

        return tokenized

    train_dataset = train_dataset.map(
        preprocess,
        batched=True,
        remove_columns=train_dataset.column_names,
    )
    eval_dataset = eval_dataset.map(
        preprocess,
        batched=True,
        remove_columns=eval_dataset.column_names,
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer,
        mlm=False
    )

    training_folder = os.path.join(settings.output_folder, "training")
    adapter_folder = os.path.join(settings.output_folder, "adapter")
    os.makedirs(training_folder, exist_ok=True)
    os.makedirs(adapter_folder, exist_ok=True)

    training_args = TrainingArguments(
        output_dir=training_folder,

        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=8,

        num_train_epochs=2,
        max_steps=200,

        learning_rate=2e-4,
        warmup_steps=100,

        fp16=False,
        bf16=False,

        eval_strategy=IntervalStrategy.EPOCH,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator
    )

    model.config.use_cache=False
    trainer.train()

    model.save_pretrained(adapter_folder)
    tokenizer.save_pretrained(adapter_folder)