from pydantic import BaseModel


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
    created_at: str
