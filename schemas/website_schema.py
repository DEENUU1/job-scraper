from pydantic import BaseModel, UUID4
from .offer_schema import OfferOutput

from typing import List


class WebsiteInput(BaseModel):
    url: str


class WebsiteOutput(BaseModel):
    id: UUID4
    url: str


class WebsiteOfferOutput(WebsiteOutput):
    offers: List[OfferOutput]
