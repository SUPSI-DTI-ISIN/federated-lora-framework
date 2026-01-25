from services.model_path import ModelPathServiceInterface, ModelPathService


def get_model_path_service() -> ModelPathServiceInterface:
    return ModelPathService.get_instance()