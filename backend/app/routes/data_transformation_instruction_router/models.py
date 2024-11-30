from pydantic import BaseModel
from typing import Any, Optional


class DataTransformationInstructionCreate(BaseModel):
    name: str
    data: Any


class DataTransformationInstructionResponse(BaseModel):
    id: int
    name: str
    data: Any

    class Config:
        orm_mode = True


class DataTransformationInstructionParams(BaseModel):
    name: Optional[str]
