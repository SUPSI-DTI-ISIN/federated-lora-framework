import os

from transformers import TrainingArguments, Trainer, IntervalStrategy, DataCollatorForLanguageModeling

from src.federated_learning_client.utils import FileUtils


class TrainingService:
    @staticmethod
    def train(model, tokenizer, train_dataset, eval_dataset, partition_id: int):
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

        training_folder = FileUtils.get_training_folder(partition_id=partition_id)
        adapter_folder = FileUtils.get_adapter_folder(partition_id=partition_id)

        training_args = TrainingArguments(
            output_dir=training_folder,

            num_train_epochs=3,
            per_device_train_batch_size=1,
            gradient_accumulation_steps=16,
            learning_rate=2e-4,

            fp16=False,
            bf16=True,
            gradient_checkpointing=True,

            optim="paged_adamw_32bit",
            weight_decay=0.01,
            warmup_ratio=0.03,
            lr_scheduler_type="cosine",

            # Logging and saving
            logging_steps=10,
            save_strategy="epoch",
            save_total_limit=3,

            # Performance settings
            max_grad_norm=0.3,
            group_by_length=True,
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=data_collator,
            packing=True,
        )

        train_output = trainer.train()

        model.save_pretrained(adapter_folder)
        tokenizer.save_pretrained(adapter_folder)

        metrics = {
            "train_loss": float(train_output.training_loss) if hasattr(train_output, "training_loss") else None,
            "hf_train_metrics": train_output.metrics if hasattr(train_output, "metrics") else None,
        }

        return metrics