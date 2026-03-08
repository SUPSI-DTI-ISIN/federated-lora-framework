from enum import Enum


class CeleryJobResultType(Enum):
    SUCCESS = "success"
    FAILURE = "failure"