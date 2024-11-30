from pydantic import BaseModel
from typing import Any, Optional


class LogCreate(BaseModel):
    model_id: int
    transformation_instruction_id: Optional[int]
    contract_id: int
    data: Any


class LogResponse(BaseModel):
    id: int
    model_id: int
    transformation_instruction_id: Optional[int]
    contract_id: int
    data: Any

    class Config:
        orm_mode = True


class LogParams(BaseModel):
    model_id: Optional[int]
    contract_id: Optional[int]
