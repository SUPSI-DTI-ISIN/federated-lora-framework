from config import settings
from .celery_client_service import CeleryClientService
from .celery_client_service_interface import CeleryClientServiceInterface

def get_celery_client_service(redis_url = settings.redis_url) -> CeleryClientServiceInterface:
    return CeleryClientService.get_instance(redis_url=redis_url)