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
    id: int
    title: str
    url: str
    page: str
    check: bool = False
    created_at: datetime


class OfferListOutput(BaseModel):
    offers: list[OfferOutput]
    prev_page: Optional[int] = None
    next_page: Optional[int] = None
