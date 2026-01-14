import os

from transformers import TrainingArguments, Trainer, IntervalStrategy, DataCollatorForLanguageModeling

class TrainingService:
    @staticmethod
    def train(model, tokenizer, train_dataset, eval_dataset):
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

        training_folder = os.path.join("./output", "training")
        adapter_folder = os.path.join("./output", "adapter")
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

        model.save_pretrained(adapter_folder)
        tokenizer.save_pretrained(adapter_folder)

        metrics = {
            "train_loss": float(train_output.training_loss) if hasattr(train_output, "training_loss") else None,
            "eval_loss": eval_metrics.get("eval_loss"),
            "hf_train_metrics": train_output.metrics if hasattr(train_output, "metrics") else None,
        }

        return metrics