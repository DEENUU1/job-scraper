from enum import Enum


class SortEnum(Enum):
    """
    An enumeration class representing sorting options.

    Attributes:
        NEWEST (str): Represents sorting by newest items.
        OLDEST (str): Represents sorting by oldest items.
    """
    NEWEST = "newest"
    OLDEST = "oldest"
