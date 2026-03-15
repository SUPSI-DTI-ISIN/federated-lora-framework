from schemas.inference import QueryRequestDTO
from schemas.model import LoadedModel
from .inference_service_interface import InferenceServiceInterface
from .tasks import inference_celery_task

class InferenceService(InferenceServiceInterface):
    __INSTANCE = None

    @classmethod
    def get_instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE


    async def inference_model(self, query_request_dto: QueryRequestDTO) -> str:
        task = inference_celery_task.delay(
            query_request_dto=query_request_dto.model_dump_json()
        )

        return task.id