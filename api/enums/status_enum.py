from enum import Enum


class StatusEnum(str, Enum):
    processing = "processing"
    success = "success"
    failure = "failure"