from celery import Celery

from .celery_client_service_interface import CeleryClientServiceInterface


class CeleryClientService(CeleryClientServiceInterface):
    __INSTANCE = None

    def __init__(self, redis_url: str, celery_worker_name: str):
        self.__celery = Celery(
            celery_worker_name,
            broker=f"{redis_url}/0",
            backend=f"{redis_url}/0",
            include=[
                "services.celery.signals",
                "services.celery.tasks",
            ]
        )

    @classmethod
    def get_instance(cls, redis_url: str, celery_worker_name: str = "worker"):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(redis_url=redis_url, celery_worker_name=celery_worker_name)
        return cls.__INSTANCE

    def get_celery_client(self) -> Celery:
        return self.__celery