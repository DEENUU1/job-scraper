from pydantic import BaseModel, UUID4


class WebsiteInput(BaseModel):
    url: str


class WebsiteOutput(BaseModel):
    id: UUID4
    url: str
