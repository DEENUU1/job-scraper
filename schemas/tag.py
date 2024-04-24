from pydantic import BaseModel


class TagOutput(BaseModel):
    name: str
