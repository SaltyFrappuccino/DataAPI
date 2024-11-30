from sqlalchemy import Column, Integer, Text, String, JSON, Boolean, Enum, ForeignKey, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from enum import Enum as PyEnum


Base = declarative_base()


class MLModel(Base):
    __tablename__ = 'ml_model'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    version = Column(String, nullable=False)

    logs = relationship('Log', back_populates='model', cascade='all, delete-orphan')
    contracts = relationship('Contract', secondary='ml_model_contract', back_populates='models')


class Contract(Base):
    __tablename__ = 'contract'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    data = Column(JSON, nullable=False)

    logs = relationship('Log', back_populates='contract', cascade='all, delete-orphan')
    models = relationship('MLModel', secondary='ml_model_contract', back_populates='contracts')
    connections = relationship('DBConnection', secondary='contract_connection', back_populates='contracts')
    transformation_instructions = relationship(
        'DataTransformationInstruction',
        secondary='contract_transformation_instruction',
        back_populates='contracts'
    )
    artifacts = relationship('Artifact', secondary='contract_artifact', back_populates='contracts')


class DBConnection(Base):
    __tablename__ = 'db_connection'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    db_type = Column(String(50), nullable=False)
    host = Column(String(255))
    port = Column(Integer)
    database = Column(String(255))
    username = Column(String(255))
    password = Column(String(255))

    contracts = relationship('Contract', secondary='contract_connection', back_populates='connections')


class DataTransformationInstruction(Base):
    __tablename__ = 'data_transformation_instruction'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    data = Column(JSON, nullable=False)

    logs = relationship('Log', back_populates='transformation_instruction', cascade='all, delete-orphan')
    contracts = relationship(
        'Contract',
        secondary='contract_transformation_instruction',
        back_populates='transformation_instructions'
    )


class Artifact(Base):
    __tablename__ = 'artifact'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    data = Column(JSON, nullable=False)

    contracts = relationship('Contract', secondary='contract_artifact', back_populates='artifacts')


class Log(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('ml_model.id', ondelete='CASCADE'), nullable=False)
    transformation_instruction_id = Column(Integer, ForeignKey('data_transformation_instruction.id', ondelete='SET NULL'))
    contract_id = Column(Integer, ForeignKey('contract.id', ondelete='CASCADE'), nullable=False)
    data = Column(JSON, nullable=False)

    model = relationship('MLModel', back_populates='logs')
    transformation_instruction = relationship('DataTransformationInstruction', back_populates='logs')
    contract = relationship('Contract', back_populates='logs')


ml_model_contract = Table(
    'ml_model_contract', Base.metadata,
    Column('ml_model_id', Integer, ForeignKey('ml_model.id', ondelete='CASCADE'), primary_key=True),
    Column('contract_id', Integer, ForeignKey('contract.id', ondelete='CASCADE'), primary_key=True)
)


contract_connection = Table(
    'contract_connection', Base.metadata,
    Column('contract_id', Integer, ForeignKey('contract.id', ondelete='CASCADE'), primary_key=True),
    Column('connection_id', Integer, ForeignKey('db_connection.id', ondelete='CASCADE'), primary_key=True)
)


contract_transformation_instruction = Table(
    'contract_transformation_instruction', Base.metadata,
    Column('contract_id', Integer, ForeignKey('contract.id', ondelete='CASCADE'), primary_key=True),
    Column('transformation_instruction_id', Integer, ForeignKey('data_transformation_instruction.id', ondelete='CASCADE'), primary_key=True)
)


contract_artifact = Table(
    'contract_artifact', Base.metadata,
    Column('contract_id', Integer, ForeignKey('contract.id', ondelete='CASCADE'), primary_key=True),
    Column('artifact_id', Integer, ForeignKey('artifact.id', ondelete='CASCADE'), primary_key=True)
)


# ------------------------------------------ old models ------------------------------------------
class BaseNode(Base):
    __tablename__ = "base_node"

    id = Column(Integer, primary_key=True, autoincrement=True)
    base_node_type = Column(String(50), nullable=False)
    label = Column(String(255), nullable=False)
    inputs = Column(JSON, nullable=True)
    outputs = Column(JSON, nullable=True)


class DataSourceNode(Base):
    __tablename__ = "data_source_node"

    class ConnectionTypeEnum(PyEnum):
        SQL = "SQL"
        NoSQL = "NoSQL"
        Streaming = "Streaming"
        File = "File"
        API = "API"

    id = Column(Integer, ForeignKey("base_node.id", ondelete="SET NULL"), primary_key=True)
    data_source_type = Column(String(50), default="data_source", nullable=False)
    connection_type = Column(Enum(ConnectionTypeEnum), nullable=False)
    subtype = Column(String(50), nullable=True)
    host = Column(String(255), nullable=False)
    port = Column(Integer, nullable=True)
    database = Column(String(255), nullable=True)
    file_path = Column(Text, nullable=True)
    credentials = Column(JSON, nullable=True)
    test_connection = Column(Boolean, default=False)


class DataTransformationNode(Base):
    __tablename__ = "data_transformation_node"

    class LanguageEnum(PyEnum):
        LanguagePython = "Python"
        LanguageJavaScript = "JavaScript"

    id = Column(Integer, ForeignKey("base_node.id", ondelete="SET NULL"), primary_key=True)
    data_transformation_node_type = Column(String(50), default="data_transformation", nullable=False)
    template = Column(String(255), nullable=True)
    script = Column(Text, nullable=True)
    language = Column(Enum(LanguageEnum), nullable=False)
    no_code_settings = Column(JSON, nullable=True)


class DataValidationNode(Base):
    __tablename__ = "data_validation_node"

    id = Column(Integer, ForeignKey("base_node.id", ondelete="SET NULL"), primary_key=True)
    data_validation_node_type = Column(String(50), default="data_validation", nullable=False)
    rules = Column(JSON, nullable=False)


class ModelNode(Base):
    __tablename__ = "model_node"

    class EnvironmentEnum(PyEnum):
        DEV = "dev"
        STAGING = "staging"
        PROD = "prod"

    id = Column(Integer, ForeignKey("base_node.id", ondelete="SET NULL"), primary_key=True)
    model_node_type = Column(String(50), default="model", nullable=False)
    environment = Column(Enum(EnvironmentEnum), nullable=False)
    model_id = Column(String(255), nullable=False)
    auth_token = Column(Text, nullable=True)
    timeout = Column(Float, nullable=True)


class LoggingNode(Base):
    __tablename__ = "logging_node"

    class NodeTypeEnum(PyEnum):
        INFO = "INFO"
        WARNING = "WARNING"
        ERROR = "ERROR"
        DEBUG = "DEBUG"

    class DestinationEnum(PyEnum):
        CONSOLE = "console"
        FILE = "file"
        EXTERNAL = "external"

    id = Column(Integer, ForeignKey("base_node.id", ondelete="SET NULL"), primary_key=True)
    logging_node_type = Column(String(50), default="logging", nullable=False)
    log_level = Column(Enum(NodeTypeEnum), nullable=False)
    destination = Column(Enum(DestinationEnum), nullable=False)
    external_config = Column(JSON, nullable=True)


class MonitoringNode(Base):
    __tablename__ = "monitoring_node"

    id = Column(Integer, ForeignKey("base_node.id", ondelete="SET NULL"), primary_key=True)
    monitoring_node_type = Column(String(50), default="monitoring", nullable=False)
    metrics = Column(JSON, nullable=False)
    alert_conditions = Column(JSON, nullable=True)
