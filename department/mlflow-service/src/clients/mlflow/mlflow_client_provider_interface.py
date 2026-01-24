from abc import ABC, abstractmethod

from mlflow.tracking import MlflowClient


class MlFlowClientProviderInterface(ABC):
    @abstractmethod
    def get_mlflow_client(self) -> MlflowClient:
        raise NotImplementedError