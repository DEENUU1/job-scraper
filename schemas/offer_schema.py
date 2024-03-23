from pydantic import BaseModel


class OfferInput(BaseModel):
    title: str
    url: str
