from pydantic import BaseModel
from typing import Optional, Any


class ContractCreate(BaseModel):
    name: str
    description: Optional[str]
    data: Any


class ContractResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    data: Any

    class Config:
        orm_mode = True


class ContractParams(BaseModel):
    name: Optional[str]
    description: Optional[str]
