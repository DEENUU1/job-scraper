from enum import Enum

class StatusEnum(str, Enum):
    """
    An enumeration class representing different statuses of an application.

    Attributes:
        NEW (str): Represents a newly created application.
        APPLICATION_SENT (str): Represents an application that has been sent.
        REJECTED (str): Represents an application that has been rejected.
        IN_PROGRESS (str): Represents an application that is currently in progress.
        APPROVED (str): Represents an application that has been approved.
    """
    NEW = "NEW"
    APPLICATION_SENT = "APPLICATION_SENT"
    REJECTED = "REJECTED"
    IN_PROGRESS = "IN_PROGRESS"
    APPROVED = "APPROVED"
