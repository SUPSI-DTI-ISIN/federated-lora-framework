from .inference_service_client_interface import InferenceServiceClientInterface
from .dependencies import get_inference_service_client

__all__ = [
    'InferenceServiceClientInterface',
    'get_inference_service_client'
]

__version__ = "1.0.0"