from config import settings
from .celery_client_interface import CeleryClientInterface
from .celery_client import CeleryClient

celery_client = CeleryClient.get_instance(settings.redis_url)
celery = celery_client.get_celery_client()

__all__ = [
    'celery'
]

__version__ = "1.0.0"