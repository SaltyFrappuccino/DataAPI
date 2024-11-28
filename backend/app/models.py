from sqlalchemy import Column, Integer, Text, String, JSON, Boolean, Enum, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base

from enum import Enum as PyEnum


Base = declarative_base()


class BaseNode(Base):
    __tablename__ = "base_node"

    id = Column(String(255), primary_key=True, autoincrement=True)
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

    id = Column(String(255), ForeignKey("base_node.id", ondelete="SET NULL"), primary_key=True)
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

    id = Column(String(255), ForeignKey("base_node.id", ondelete="SET NULL"), primary_key=True)
    data_transformation_node_type = Column(String(50), default="data_transformation", nullable=False)
    template = Column(String(255), nullable=True)
    script = Column(Text, nullable=True)
    language = Column(Enum(LanguageEnum), nullable=False)
    no_code_settings = Column(JSON, nullable=True)


class DataValidationNode(Base):
    __tablename__ = "data_validation_node"

    id = Column(String(255), ForeignKey("base_node.id", ondelete="SET NULL"), primary_key=True)
    data_validation_node_type = Column(String(50), default="data_validation", nullable=False)
    rules = Column(JSON, nullable=False)


class ModelNode(Base):
    __tablename__ = "model_node"

    class EnvironmentEnum(PyEnum):
        DEV = "dev"
        STAGING = "staging"
        PROD = "prod"

    id = Column(String(255), ForeignKey("base_node.id", ondelete="SET NULL"), primary_key=True)
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

    id = Column(String(255), ForeignKey("base_node.id", ondelete="SET NULL"), primary_key=True)
    logging_node_type = Column(String(50), default="logging", nullable=False)
    log_level = Column(Enum(NodeTypeEnum), nullable=False)
    destination = Column(Enum(DestinationEnum), nullable=False)
    external_config = Column(JSON, nullable=True)


class MonitoringNode(Base):
    __tablename__ = "monitoring_node"

    id = Column(String(255), ForeignKey("base_node.id", ondelete="SET NULL"), primary_key=True)
    monitoring_node_type = Column(String(50), default="monitoring", nullable=False)
    metrics = Column(JSON, nullable=False)
    alert_conditions = Column(JSON, nullable=True)
