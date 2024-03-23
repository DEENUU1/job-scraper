from pydantic import BaseModel, UUID4
from enums.status import StatusEnum


class OfferInput(BaseModel):
    title: str
    url: str


class OfferOutput(BaseModel):
    id: UUID4
    title: str
    url: str
    archived: bool = True
    status: StatusEnum
    website_id: UUID4
