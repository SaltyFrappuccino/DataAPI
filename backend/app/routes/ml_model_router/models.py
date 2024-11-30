from pydantic import BaseModel
from typing import Optional


class MLModelResponse(BaseModel):
    id: int
    name: str
    description: str | None
    version: str

    class Config:
        orm_mode = True


class MLModelParams(BaseModel):
    name: str | None
    version: str | None


class MLModelCreate(BaseModel):
    name: str
    description: Optional[str]
    version: str
