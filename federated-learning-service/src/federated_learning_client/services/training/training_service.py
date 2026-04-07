import math

import torch

from typing import Optional
from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling

from src.federated_learning_client.utils import Llama2Utils, FileUtils


class TrainingService:
    @staticmethod
    def __preprocess(examples, tokenizer, max_length: int = 512):
        full_texts = []
        prompt_lengths = []

        for i in range(len(examples["instruction"])):
            system = examples["instruction"][i]
            user = examples["input"][i]
            assistant = examples["output"][i]

            formatted = Llama2Utils.format_chat(system=system, user=user, assistant=assistant)

            full_text = formatted["text"]
            prompt_length = int(formatted["prompt_length"])

            full_texts.append(full_text)
            prompt_lengths.append(prompt_length)

        tokenized = tokenizer(
            full_texts,
            max_length=max_length,
            truncation=True,
            padding=False,
        )

        labels = []
        for i, ids in enumerate(tokenized["input_ids"]):
            prompt_token_count = len(tokenizer(
                full_texts[i][:prompt_lengths[i]],
                truncation=True,
                max_length=max_length,
            )["input_ids"])

            masked = [-100] * prompt_token_count + ids[prompt_token_count:]
            labels.append(masked)

        tokenized["labels"] = labels
        return tokenized

    @staticmethod
    def __get_precision_flags():
        use_cpu = fp16 = bf16 = False
        if not torch.cuda.is_available():
            use_cpu = True
        else:
            try:
                bf16_supported = getattr(torch.cuda, "is_bf16_supported", lambda: False)()
            except Exception:
                bf16_supported = False
            bf16 = bf16_supported
            fp16 = not bf16_supported
        return use_cpu, fp16, bf16

    @classmethod
    def train(cls, model, tokenizer, train_dataset, partition_id: Optional[int] = None):
        use_cpu, fp16, bf16 = cls.__get_precision_flags()

        train_dataset = train_dataset.map(
            lambda examples: cls.__preprocess(examples, tokenizer),
            batched=True,
            remove_columns=train_dataset.column_names,
        )

        data_collator = DataCollatorForLanguageModeling(
            tokenizer,
            mlm=False
        )

        training_folder = FileUtils.get_training_folder(partition_id=partition_id)
        adapter_folder = FileUtils.get_adapter_folder(partition_id=partition_id)

        training_args = TrainingArguments(
            output_dir=training_folder,

            num_train_epochs=3,
            per_device_train_batch_size=1,
            gradient_accumulation_steps=16,
            learning_rate=2e-4,

            fp16=fp16,
            bf16=bf16,
            use_cpu=use_cpu,
            gradient_checkpointing=True,

            optim="paged_adamw_32bit",
            weight_decay=0.01,
            warmup_ratio=0.03,
            lr_scheduler_type="cosine",

            # Logging and saving
            logging_steps=10,
            save_strategy="epoch",
            save_total_limit=3,

            max_grad_norm=0.3,
            group_by_length=True,
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            data_collator=data_collator,
        )

        train_output = trainer.train()

        model.save_pretrained(adapter_folder)
        tokenizer.save_pretrained(adapter_folder)

        print(f"Train output {train_output}")

        metrics = {
            "train_loss": train_output.metrics.get("train_loss", 0.0),
            "num-examples": int(len(train_dataset)),
        }

        return metrics

    @classmethod
    def evaluate(cls, model, tokenizer, eval_dataset, partition_id: Optional[int] = None):
        use_cpu, fp16, bf16 = cls.__get_precision_flags()

        eval_dataset = eval_dataset.map(
            lambda examples: cls.__preprocess(examples, tokenizer),
            batched=True,
            remove_columns=eval_dataset.column_names,
        )

        data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)
        model.eval()

        training_folder = FileUtils.get_training_folder(partition_id=partition_id)

        training_args = TrainingArguments(
            output_dir=training_folder,
            fp16=fp16,
            bf16=bf16,
            use_cpu=use_cpu,
            gradient_checkpointing=False,
            per_device_eval_batch_size=2,
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            eval_dataset=eval_dataset,
            data_collator=data_collator,
        )

        evaluate_output = trainer.evaluate()
        eval_loss = evaluate_output.get("eval_loss", float("inf"))

        try:
            eval_perplexity = math.exp(eval_loss)
        except OverflowError:
            eval_perplexity = float("inf")

        return eval_loss, eval_perplexity
