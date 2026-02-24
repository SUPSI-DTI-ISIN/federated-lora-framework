from abc import ABC, abstractmethod

from starlette.requests import Request


class SseServiceInterface(ABC):
    @abstractmethod
    async def generate_sse_events(self, request: Request):
        raise NotImplementedError