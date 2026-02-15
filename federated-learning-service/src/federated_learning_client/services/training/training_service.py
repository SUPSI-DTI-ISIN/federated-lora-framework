import torch

from typing import Optional
from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling

from src.federated_learning_client.utils import FileUtils


class TrainingService:
    @staticmethod
    def train(model, tokenizer, train_dataset, eval_dataset, partition_id: Optional[int] = None):

        print("torch version:", torch.__version__)
        print("cuda available:", torch.cuda.is_available())
        if torch.cuda.is_available():
            try:
                props = torch.cuda.get_device_properties(0)
                print("device name:", props.name)
                print("total mem (GB):", props.total_memory / (1024**3))
                print("compute capability:", props.major, props.minor)
            except Exception as e:
                print("Errore ottenendo properties:", e)

        print("torch.cuda.is_bf16_supported:", getattr(torch.cuda, "is_bf16_supported", lambda: False)())


        use_cpu = False
        fp16 = False
        bf16 = False
        if not torch.cuda.is_available():
            use_cpu = True
        else:
            try:
                bf16_supported = getattr(torch.cuda, "is_bf16_supported", lambda: False)()
            except Exception:
                bf16_supported = False

            if bf16_supported:
                bf16 = True
            else:
                fp16 = True

        print(f"use_cpu: {use_cpu}")
        print(f"bf16: {bf16}")
        print(f"fp16: {fp16}")

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