from typing import Optional

from celery import Celery

from .celery_client_interface import CeleryClientInterface


class CeleryClient(CeleryClientInterface):
    __INSTANCE = None

    def __init__(self, redis_url: str, celery_worker_name: str):
        self.__celery = Celery(
            celery_worker_name,
            broker=f"{redis_url}/0",
            backend=f"{redis_url}/0",
            include=[
                "services.job.signals",
                "services.job.tasks",
            ]
        )

    @classmethod
    def get_instance(cls, redis_url: str, celery_worker_name: Optional[str] = "worker"):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls(redis_url=redis_url, celery_worker_name=celery_worker_name)
        return cls.__INSTANCE

    def get_celery_client(self) -> Celery:
        return self.__celery