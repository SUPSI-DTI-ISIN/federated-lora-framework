import math
import pytest
from unittest.mock import MagicMock, patch

from src.federated_learning_client.services.training.training_service import TrainingService


class TestGetPrecisionFlags:
    def test_returns_cpu_true_when_cuda_not_available(self):
        with patch("src.federated_learning_client.services.training.training_service.torch") as mock_torch:
            mock_torch.cuda.is_available.return_value = False
            use_cpu, fp16, bf16 = TrainingService._TrainingService__get_precision_flags()

        assert use_cpu is True
        assert fp16 is False
        assert bf16 is False

    def test_returns_bf16_when_cuda_available_and_bf16_supported(self):
        with patch("src.federated_learning_client.services.training.training_service.torch") as mock_torch:
            mock_torch.cuda.is_available.return_value = True
            mock_torch.cuda.is_bf16_supported.return_value = True
            use_cpu, fp16, bf16 = TrainingService._TrainingService__get_precision_flags()

        assert use_cpu is False
        assert bf16 is True
        assert fp16 is False

    def test_returns_fp16_when_cuda_available_but_bf16_not_supported(self):
        with patch("src.federated_learning_client.services.training.training_service.torch") as mock_torch:
            mock_torch.cuda.is_available.return_value = True
            mock_torch.cuda.is_bf16_supported.return_value = False
            use_cpu, fp16, bf16 = TrainingService._TrainingService__get_precision_flags()

        assert use_cpu is False
        assert fp16 is True
        assert bf16 is False

    def test_handles_exception_in_bf16_check(self):
        with patch("src.federated_learning_client.services.training.training_service.torch") as mock_torch:
            mock_torch.cuda.is_available.return_value = True
            mock_torch.cuda.is_bf16_supported.side_effect = RuntimeError("not supported")
            use_cpu, fp16, bf16 = TrainingService._TrainingService__get_precision_flags()

        assert fp16 is True
        assert bf16 is False


class TestBuildMessages:
    def test_returns_three_messages(self):
        msgs = TrainingService._TrainingService__build_messages("sys", "user", "assistant")
        assert len(msgs) == 3

    def test_roles_are_correct(self):
        msgs = TrainingService._TrainingService__build_messages("sys", "user", "assistant")
        assert msgs[0]["role"] == "system"
        assert msgs[1]["role"] == "user"
        assert msgs[2]["role"] == "assistant"

    def test_content_is_correct(self):
        msgs = TrainingService._TrainingService__build_messages("S", "U", "A")
        assert msgs[0]["content"] == "S"
        assert msgs[1]["content"] == "U"
        assert msgs[2]["content"] == "A"


class TestBuildPromptMessages:
    def test_returns_two_messages(self):
        msgs = TrainingService._TrainingService__build_prompt_messages("sys", "user")
        assert len(msgs) == 2

    def test_roles_are_correct(self):
        msgs = TrainingService._TrainingService__build_prompt_messages("sys", "user")
        assert msgs[0]["role"] == "system"
        assert msgs[1]["role"] == "user"


class TestEvaluate:
    def test_returns_eval_loss_and_perplexity(self):
        model = MagicMock()
        tokenizer = MagicMock()
        eval_dataset = MagicMock()
        eval_dataset.column_names = ["instruction", "input", "output"]
        eval_dataset.map.return_value = eval_dataset

        mock_trainer = MagicMock()
        mock_trainer.evaluate.return_value = {"eval_loss": 1.0}

        with patch("src.federated_learning_client.services.training.training_service.TrainingArguments"), \
             patch("src.federated_learning_client.services.training.training_service.Trainer",
                   return_value=mock_trainer), \
             patch("src.federated_learning_client.services.training.training_service.DataCollatorForLanguageModeling"), \
             patch("src.federated_learning_client.services.training.training_service.FileUtils.get_training_folder",
                   return_value="/tmp/training"), \
             patch("src.federated_learning_client.services.training.training_service.TrainingService._TrainingService__get_precision_flags",
                   return_value=(True, False, False)):
            loss, perplexity = TrainingService.evaluate(
                model=model, tokenizer=tokenizer, eval_dataset=eval_dataset
            )

        assert loss == 1.0
        assert abs(perplexity - math.exp(1.0)) < 0.001

    def test_returns_inf_perplexity_on_overflow(self):
        model = MagicMock()
        tokenizer = MagicMock()
        eval_dataset = MagicMock()
        eval_dataset.column_names = []
        eval_dataset.map.return_value = eval_dataset

        mock_trainer = MagicMock()
        mock_trainer.evaluate.return_value = {"eval_loss": float("inf")}

        with patch("src.federated_learning_client.services.training.training_service.TrainingArguments"), \
             patch("src.federated_learning_client.services.training.training_service.Trainer",
                   return_value=mock_trainer), \
             patch("src.federated_learning_client.services.training.training_service.DataCollatorForLanguageModeling"), \
             patch("src.federated_learning_client.services.training.training_service.FileUtils.get_training_folder",
                   return_value="/tmp/training"), \
             patch("src.federated_learning_client.services.training.training_service.TrainingService._TrainingService__get_precision_flags",
                   return_value=(True, False, False)):
            loss, perplexity = TrainingService.evaluate(
                model=model, tokenizer=tokenizer, eval_dataset=eval_dataset
            )

        assert perplexity == float("inf")

    def test_returns_default_inf_loss_when_key_missing(self):
        model = MagicMock()
        tokenizer = MagicMock()
        eval_dataset = MagicMock()
        eval_dataset.column_names = []
        eval_dataset.map.return_value = eval_dataset

        mock_trainer = MagicMock()
        mock_trainer.evaluate.return_value = {}  # no eval_loss key

        with patch("src.federated_learning_client.services.training.training_service.TrainingArguments"), \
             patch("src.federated_learning_client.services.training.training_service.Trainer",
                   return_value=mock_trainer), \
             patch("src.federated_learning_client.services.training.training_service.DataCollatorForLanguageModeling"), \
             patch("src.federated_learning_client.services.training.training_service.FileUtils.get_training_folder",
                   return_value="/tmp/training"), \
             patch("src.federated_learning_client.services.training.training_service.TrainingService._TrainingService__get_precision_flags",
                   return_value=(True, False, False)):
            loss, perplexity = TrainingService.evaluate(
                model=model, tokenizer=tokenizer, eval_dataset=eval_dataset
            )

        assert loss == float("inf")
        assert perplexity == float("inf")


class TestTrain:
    def test_returns_metrics_dict(self):
        model = MagicMock()
        tokenizer = MagicMock()
        train_dataset = MagicMock()
        train_dataset.column_names = ["instruction", "input", "output"]
        train_dataset.map.return_value = train_dataset

        mock_train_output = MagicMock()
        mock_train_output.metrics = {"train_loss": 0.5}

        mock_trainer = MagicMock()
        mock_trainer.train.return_value = mock_train_output

        with patch("src.federated_learning_client.services.training.training_service.TrainingArguments"), \
             patch("src.federated_learning_client.services.training.training_service.Trainer",
                   return_value=mock_trainer), \
             patch("src.federated_learning_client.services.training.training_service.DataCollatorForLanguageModeling"), \
             patch("src.federated_learning_client.services.training.training_service.FileUtils.get_training_folder",
                   return_value="/tmp/training"), \
             patch("src.federated_learning_client.services.training.training_service.FileUtils.get_adapter_folder",
                   return_value="/tmp/adapter"), \
             patch("src.federated_learning_client.services.training.training_service.TrainingService._TrainingService__get_precision_flags",
                   return_value=(True, False, False)):
            metrics = TrainingService.train(
                model=model, tokenizer=tokenizer, train_dataset=train_dataset
            )

        assert "train_loss" in metrics
        assert "num-examples" in metrics
        assert metrics["train_loss"] == 0.5

    def test_saves_model_and_tokenizer(self):
        model = MagicMock()
        tokenizer = MagicMock()
        train_dataset = MagicMock()
        train_dataset.column_names = []
        train_dataset.map.return_value = train_dataset

        mock_train_output = MagicMock()
        mock_train_output.metrics = {}

        mock_trainer = MagicMock()
        mock_trainer.train.return_value = mock_train_output

        with patch("src.federated_learning_client.services.training.training_service.TrainingArguments"), \
             patch("src.federated_learning_client.services.training.training_service.Trainer",
                   return_value=mock_trainer), \
             patch("src.federated_learning_client.services.training.training_service.DataCollatorForLanguageModeling"), \
             patch("src.federated_learning_client.services.training.training_service.FileUtils.get_training_folder",
                   return_value="/tmp/training"), \
             patch("src.federated_learning_client.services.training.training_service.FileUtils.get_adapter_folder",
                   return_value="/tmp/adapter"), \
             patch("src.federated_learning_client.services.training.training_service.TrainingService._TrainingService__get_precision_flags",
                   return_value=(True, False, False)):
            TrainingService.train(model=model, tokenizer=tokenizer, train_dataset=train_dataset)

        model.save_pretrained.assert_called_once_with("/tmp/adapter")
        tokenizer.save_pretrained.assert_called_once_with("/tmp/adapter")


class TestTrainingServiceInit:
    def test_exports_training_service(self):
        from src.federated_learning_client.services.training import TrainingService as TS
        assert TS is TrainingService

    def test_version(self):
        from src.federated_learning_client.services.training import __version__
        assert __version__ == "1.0.0"
