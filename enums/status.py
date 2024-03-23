from enum import Enum


class StatusEnum(str, Enum):
    NEW = "NEW"
    APPLICATION_SENT = "APPLICATION_SENT"
    REJECTED = "REJECTED"
    IN_PROGRESS = "IN_PROGRESS"
    APPROVED = "APPROVED"
