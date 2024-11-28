from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional, List

# Database Configuration
DATABASE_URL = "mysql+mysqlconnector://root@localhost/data_api"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI()


# Models for ORM
class DataSource(Base):
    __tablename__ = "DataSources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    source_type = Column(String(255), nullable=False)
    status = Column(Enum("active", "inactive"), default="active")
    data = Column(JSON)


class DataTransformation(Base):
    __tablename__ = "DataTransformations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    input_data_type = Column(String(255), nullable=False)
    data = Column(JSON)


class Model(Base):
    __tablename__ = "Models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    connection_type = Column(String(255), nullable=False)
    version = Column(String(50))
    cover_path = Column(String(255))


Base.metadata.create_all(bind=engine)


# Pydantic Schemas
class DataSourceSchema(BaseModel):
    id: Optional[int] = None
    name: str
    source_type: str
    status: Optional[str] = "active"
    data: dict

    class Config:
        orm_mode = True


class DataTransformationSchema(BaseModel):
    id: Optional[int] = None
    name: str
    input_data_type: str
    data: dict

    class Config:
        orm_mode = True


class ModelSchema(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str]
    connection_type: str
    version: Optional[str]
    cover_path: Optional[str]

    class Config:
        orm_mode = True


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD Operations for DataSources
@app.get("/datasources", response_model=List[DataSourceSchema])
def get_datasources(db: Session = Depends(get_db)):
    return db.query(DataSource).all()


@app.post("/datasources", response_model=DataSourceSchema)
def create_datasource(datasource: DataSourceSchema, db: Session = Depends(get_db)):
    db_item = DataSource(**datasource.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
