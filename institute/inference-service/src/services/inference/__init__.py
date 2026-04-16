from .inference_service_interface import InferenceServiceInterface
from .dependencies import get_inference_service

__all__ = [
    'InferenceServiceInterface',
    'get_inference_service'
]

__version__ = "1.0.0"