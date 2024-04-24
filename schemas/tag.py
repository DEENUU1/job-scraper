from pydantic import BaseModel
from typing import Optional


class TagOutput(BaseModel):
    name: Optional[str] = None
