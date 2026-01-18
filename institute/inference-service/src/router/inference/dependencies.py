from services import InferenceServiceInterface, InferenceService

def get_inference_service() -> InferenceServiceInterface:
    return InferenceService()