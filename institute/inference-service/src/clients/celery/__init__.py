from .celery_client_service_interface import CeleryClientServiceInterface
from .celery_client_service import CeleryClientService
from .dependencies import get_celery_client_service

celery = get_celery_client_service().get_celery_client()

__all__ = [
    'get_celery_client_service'
]

__version__ = "1.0.0"