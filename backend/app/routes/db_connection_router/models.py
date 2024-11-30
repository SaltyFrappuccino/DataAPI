from pydantic import BaseModel
from typing import Optional


class DBConnectionCreate(BaseModel):
    name: str
    db_type: str
    host: Optional[str]
    port: Optional[int]
    database: Optional[str]
    username: Optional[str]
    password: Optional[str]


class DBConnectionResponse(BaseModel):
    id: int
    name: str
    db_type: str
    host: Optional[str]
    port: Optional[int]
    database: Optional[str]
    username: Optional[str]
    password: Optional[str]

    class Config:
        orm_mode = True


class DBConnectionParams(BaseModel):
    name: Optional[str]
    db_type: Optional[str]
