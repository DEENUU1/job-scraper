from pydantic import BaseModel
from datetime import datetime

from typing import Optional


class Offer(BaseModel):
    """
    Pydantic BaseModel representing input data for an offer.

    Attributes:
        title (str): The title of the offer.
        url (str): The URL associated with the offer.
    """
    title: str
    url: str


class OfferOutput(BaseModel):
    """
    Represents an offer returned from the API.

    Attributes:
        id (int): The unique identifier of the offer.
        title (str): The title of the offer.
        url (str): The URL of the offer.
        page (str): The page where the offer was found.
        check (bool, optional): A flag indicating if the offer has been checked. Defaults to False.
        created_at (datetime): The date and time when the offer was created in the system.
    """

    id: int
    title: str
    url: str
    page: str
    check: bool = False
    created_at: datetime


class OfferListOutput(BaseModel):
    """
    Represents a list of offers along with pagination information.

    Attributes:
        offers (list[OfferOutput]): A list of `OfferOutput` objects.
        prev_page (int, optional): The index of the previous page, if it exists. Defaults to None.
        next_page (int, optional): The index of the next page, if it exists. Defaults to None.
    """

    offers: list[OfferOutput]
    prev_page: Optional[int] = None
    next_page: Optional[int] = None
    query: Optional[str] = None
    sort_by: Optional[str] = None
