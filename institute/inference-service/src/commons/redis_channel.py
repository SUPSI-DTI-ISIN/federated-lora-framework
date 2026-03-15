from enum import Enum


class RedisChannel(Enum):
    INFERENCE_RESULT = "inference:result"