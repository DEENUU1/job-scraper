from pydantic import BaseModel, UUID4
from datetime import datetime


class OfferInput(BaseModel):
    title: str
    url: str


class OfferOutput(BaseModel):
    id: UUID4
    title: str
    url: str
    archived: bool = True
    status: str
    website_id: UUID4
    created_at: datetime