class FederatedLearningJobNotFoundError(Exception):
    def __init__(self, federated_learning_job_id: int):
        self.federated_learning_job_id = federated_learning_job_id
        super().__init__(f"Federated Learning Job with id '{federated_learning_job_id}' not found.")

class StartFederatedLearningJobFoundError(Exception):
    def __init__(self, federated_learning_job_id: int):
        self.federated_learning_job_id = federated_learning_job_id
        super().__init__(f"There is a federated learning job with id '{federated_learning_job_id}' which has not finished yet.")