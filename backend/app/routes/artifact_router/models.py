from pydantic import BaseModel
from typing import Any, Optional


class ArtifactCreate(BaseModel):
    name: str
    data: Any


class ArtifactResponse(BaseModel):
    id: int
    name: str
    data: Any

    class Config:
        orm_mode = True


class ArtifactParams(BaseModel):
    name: Optional[str]
