from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from fastapi.middleware.cors import CORSMiddleware


# Database connection setup
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/DataAPI"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Many-to-Many Tables
ml_model_contract_table = Table(
    "ml_model_contract",
    Base.metadata,
    Column("ml_model_id", Integer, ForeignKey("ml_model.id", ondelete="CASCADE"), primary_key=True),
    Column("contract_id", Integer, ForeignKey("contract.id", ondelete="CASCADE"), primary_key=True),
)

contract_connection_table = Table(
    "contract_connection",
    Base.metadata,
    Column("contract_id", Integer, ForeignKey("contract.id", ondelete="CASCADE"), primary_key=True),
    Column("connection_id", Integer, ForeignKey("db_connection.id", ondelete="CASCADE"), primary_key=True),
)

contract_transformation_instruction_table = Table(
    "contract_transformation_instruction",
    Base.metadata,
    Column("contract_id", Integer, ForeignKey("contract.id", ondelete="CASCADE"), primary_key=True),
    Column("transformation_instruction_id", Integer, ForeignKey("data_transformation_instruction.id", ondelete="CASCADE"), primary_key=True),
)

contract_artifact_table = Table(
    "contract_artifact",
    Base.metadata,
    Column("contract_id", Integer, ForeignKey("contract.id", ondelete="CASCADE"), primary_key=True),
    Column("artifact_id", Integer, ForeignKey("artifact.id", ondelete="CASCADE"), primary_key=True),
)

# SQLAlchemy Models
class MLModel(Base):
    __tablename__ = "ml_model"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    version = Column(String, nullable=False)
    contracts = relationship("Contract", secondary=ml_model_contract_table, back_populates="ml_models")

class Contract(Base):
    __tablename__ = "contract"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    data = Column(JSON, nullable=False)
    ml_models = relationship("MLModel", secondary=ml_model_contract_table, back_populates="contracts")
    connections = relationship("DBConnection", secondary=contract_connection_table, back_populates="contracts")
    transformation_instructions = relationship(
        "DataTransformationInstruction", secondary=contract_transformation_instruction_table, back_populates="contracts"
    )
    artifacts = relationship("Artifact", secondary=contract_artifact_table, back_populates="contracts")

class DBConnection(Base):
    __tablename__ = "db_connection"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    db_type = Column(String(50), nullable=False)
    host = Column(String(255))
    port = Column(Integer)
    database = Column(String(255))
    username = Column(String(255))
    password = Column(String(255))
    contracts = relationship("Contract", secondary=contract_connection_table, back_populates="connections")

class DataTransformationInstruction(Base):
    __tablename__ = "data_transformation_instruction"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    data = Column(JSON, nullable=False)
    contracts = relationship(
        "Contract", secondary=contract_transformation_instruction_table, back_populates="transformation_instructions"
    )

class Artifact(Base):
    __tablename__ = "artifact"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    data = Column(JSON, nullable=False)
    contracts = relationship("Contract", secondary=contract_artifact_table, back_populates="artifacts")

class Log(Base):
    __tablename__ = "log"
    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("ml_model.id", ondelete="CASCADE"), nullable=False)
    transformation_instruction_id = Column(Integer, ForeignKey("data_transformation_instruction.id", ondelete="SET NULL"))
    contract_id = Column(Integer, ForeignKey("contract.id", ondelete="CASCADE"), nullable=False)
    data = Column(JSON, nullable=False)

# Pydantic Schemas
class MLModelBase(BaseModel):
    name: str
    description: Optional[str] = None
    version: str

class MLModelResponse(MLModelBase):
    id: int

    class Config:
        orm_mode = True

class ContractBase(BaseModel):
    name: str
    description: Optional[str] = None
    data: dict

class ContractResponse(ContractBase):
    id: int

    class Config:
        orm_mode = True

class DBConnectionBase(BaseModel):
    name: str
    db_type: str
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

class DBConnectionResponse(DBConnectionBase):
    id: int

    class Config:
        orm_mode = True

class DataTransformationInstructionBase(BaseModel):
    name: str
    data: dict

class DataTransformationInstructionResponse(DataTransformationInstructionBase):
    id: int

    class Config:
        orm_mode = True

class ArtifactBase(BaseModel):
    name: str
    data: dict

class ArtifactResponse(ArtifactBase):
    id: int

    class Config:
        orm_mode = True

class LogBase(BaseModel):
    model_id: int
    transformation_instruction_id: Optional[int]
    contract_id: int
    data: dict

class LogResponse(LogBase):
    id: int

    class Config:
        orm_mode = True

# FastAPI Application
app = FastAPI(title="Data API", description="RESTful API for managing DataAPI system.", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно указать конкретные домены, например: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все HTTP методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# General CRUD operations
def create_resource(db, model, schema):
    db_obj = model(**schema.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_resource(db, model, resource_id):
    return db.query(model).filter(model.id == resource_id).first()

def list_resources(db, model):
    return db.query(model).all()

# Example Routes for MLModel
@app.post("/ml_models", response_model=MLModelResponse)
def create_ml_model(ml_model: MLModelBase, db: Session = Depends(get_db)):
    return create_resource(db, MLModel, ml_model)

@app.get("/ml_models", response_model=List[MLModelResponse])
def get_ml_models(db: Session = Depends(get_db)):
    return list_resources(db, MLModel)

@app.get("/ml_models/{id}", response_model=MLModelResponse)
def get_ml_model_by_id(id: int, db: Session = Depends(get_db)):
    db_model = get_resource(db, MLModel, id)
    if not db_model:
        raise HTTPException(status_code=404, detail="MLModel not found")
    return db_model

# Routes for Contract
@app.post("/contracts", response_model=ContractResponse)
def create_contract(contract: ContractBase, db: Session = Depends(get_db)):
    return create_resource(db, Contract, contract)

@app.get("/contracts", response_model=List[ContractResponse])
def get_contracts(db: Session = Depends(get_db)):
    return list_resources(db, Contract)

@app.get("/contracts/{id}", response_model=ContractResponse)
def get_contract_by_id(id: int, db: Session = Depends(get_db)):
    db_contract = get_resource(db, Contract, id)
    if not db_contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return db_contract

# Routes for DBConnection
@app.post("/db_connections", response_model=DBConnectionResponse)
def create_db_connection(db_connection: DBConnectionBase, db: Session = Depends(get_db)):
    return create_resource(db, DBConnection, db_connection)

@app.get("/db_connections", response_model=List[DBConnectionResponse])
def get_db_connections(db: Session = Depends(get_db)):
    return list_resources(db, DBConnection)

@app.get("/db_connections/{id}", response_model=DBConnectionResponse)
def get_db_connection_by_id(id: int, db: Session = Depends(get_db)):
    db_connection = get_resource(db, DBConnection, id)
    if not db_connection:
        raise HTTPException(status_code=404, detail="DB Connection not found")
    return db_connection

# Routes for Artifact
@app.post("/artifacts", response_model=ArtifactResponse)
def create_artifact(artifact: ArtifactBase, db: Session = Depends(get_db)):
    return create_resource(db, Artifact, artifact)

@app.get("/artifacts", response_model=List[ArtifactResponse])
def get_artifacts(db: Session = Depends(get_db)):
    return list_resources(db, Artifact)

@app.get("/artifacts/{id}", response_model=ArtifactResponse)
def get_artifact_by_id(id: int, db: Session = Depends(get_db)):
    db_artifact = get_resource(db, Artifact, id)
    if not db_artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return db_artifact

# Routes for DataTransformationInstruction
@app.post("/data_transformation_instructions", response_model=DataTransformationInstructionResponse)
def create_transformation_instruction(transformation_instruction: DataTransformationInstructionBase, db: Session = Depends(get_db)):
    return create_resource(db, DataTransformationInstruction, transformation_instruction)

@app.get("/data_transformation_instructions", response_model=List[DataTransformationInstructionResponse])
def get_transformation_instructions(db: Session = Depends(get_db)):
    return list_resources(db, DataTransformationInstruction)

@app.get("/data_transformation_instructions/{id}", response_model=DataTransformationInstructionResponse)
def get_transformation_instruction_by_id(id: int, db: Session = Depends(get_db)):
    db_instruction = get_resource(db, DataTransformationInstruction, id)
    if not db_instruction:
        raise HTTPException(status_code=404, detail="Transformation Instruction not found")
    return db_instruction

# Routes for Log
@app.post("/logs", response_model=LogResponse)
def create_log(log: LogBase, db: Session = Depends(get_db)):
    return create_resource(db, Log, log)

@app.get("/logs", response_model=List[LogResponse])
def get_logs(db: Session = Depends(get_db)):
    return list_resources(db, Log)

@app.get("/logs/{id}", response_model=LogResponse)
def get_log_by_id(id: int, db: Session = Depends(get_db)):
    db_log = get_resource(db, Log, id)
    if not db_log:
        raise HTTPException(status_code=404, detail="Log not found")
    return db_log