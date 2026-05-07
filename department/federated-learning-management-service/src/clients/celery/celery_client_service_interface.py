from abc import ABC, abstractmethod

from celery import Celery


class CeleryClientServiceInterface(ABC):
    @abstractmethod
    def get_celery_client(self) -> Celery:
        raise NotImplementedError