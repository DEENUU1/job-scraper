from pydantic import BaseModel


class OfferStatusUpdate(BaseModel):
    offer_id: int
    status: bool
