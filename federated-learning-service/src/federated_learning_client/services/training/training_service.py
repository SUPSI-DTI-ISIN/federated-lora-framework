import math

import torch

from typing import Optional
from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling

from src.federated_learning_client.utils import FileUtils


class TrainingService:
    @staticmethod
    def __build_messages(system: str, user: str, assistant: str) -> list:
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
        ]

    @staticmethod
    def __build_prompt_messages(system: str, user: str) -> list:
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

    @classmethod
    def __preprocess(cls, examples, tokenizer, max_length: int = 1024):
        all_input_ids = []
        all_attention_masks = []
        all_labels = []

        for i in range(len(examples["instruction"])):
            system = examples["instruction"][i]
            user = examples["input"][i]
            assistant = examples["output"][i]

            full_messages = cls.__build_messages(system, user, assistant)
            full_text = tokenizer.apply_chat_template(
                full_messages,
                tokenize=False,
                add_generation_prompt=False,
            )

            prompt_messages = cls.__build_prompt_messages(system, user)
            prompt_text = tokenizer.apply_chat_template(
                prompt_messages,
                tokenize=False,
                add_generation_prompt=True,
            )

            full_tokenized = tokenizer(
                full_text,
                max_length=max_length,
                truncation=True,
                padding=False,
            )
            prompt_tokenized = tokenizer(
                prompt_text,
                max_length=max_length,
                truncation=True,
                padding=False,
            )

            input_ids = full_tokenized["input_ids"]
            prompt_len = len(prompt_tokenized["input_ids"])
            labels = [-100] * prompt_len + input_ids[prompt_len:]

            all_input_ids.append(input_ids)
            all_attention_masks.append(full_tokenized["attention_mask"])
            all_labels.append(labels)

        return {
            "input_ids": all_input_ids,
            "attention_mask": all_attention_masks,
            "labels": all_labels,
        }

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
