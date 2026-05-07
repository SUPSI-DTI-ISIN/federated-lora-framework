from .inference_service import InferenceService
from .inference_service_interface import InferenceServiceInterface

def get_inference_service() -> InferenceServiceInterface:
    return InferenceService.get_instance()