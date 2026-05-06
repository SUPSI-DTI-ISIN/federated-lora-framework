from schemas.exceptions.federated_learning_job_errors import StartFederatedLearningJobFoundError


class TestStartFederatedLearningJobFoundError:
    def test_stores_job_id(self):
        assert StartFederatedLearningJobFoundError(federated_learning_job_id=42).federated_learning_job_id == 42

    def test_message_contains_id(self):
        assert "42" in str(StartFederatedLearningJobFoundError(federated_learning_job_id=42))

    def test_is_exception_subclass(self):
        assert issubclass(StartFederatedLearningJobFoundError, Exception)


class TestExceptionsInit:
    def test_exported_from_package(self):
        from schemas.exceptions import StartFederatedLearningJobFoundError as E
        assert E is StartFederatedLearningJobFoundError

    def test_version(self):
        import schemas.exceptions as e
        assert e.__version__ == "1.0.0"

    def test_all_list(self):
        import schemas.exceptions as e
        assert "StartFederatedLearningJobFoundError" in e.__all__
