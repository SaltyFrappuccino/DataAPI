from fastapi import Query
from pydantic import BaseModel, Field
from typing import Optional, Dict, List


class NodeSourceParams:
    def __init__(
        self,
        type_node: str = Query(..., description="Тип ноды")
    ):
        self.type_node = type_node


class BaseNodeBase(BaseModel):
    id: str = Field(..., description="Уникальный идентификатор узла")
    base_node_type: str = Field(..., description="Тип базового узла")
    label: str = Field(..., description="Название узла")
    inputs: Optional[Dict[str, List[str]]] = Field(None, description="Входные данные узла")
    outputs: Optional[Dict[str, List[str]]] = Field(None, description="Выходные данные узла")


class DataSourceResponse(BaseNodeBase):
    data_source_type: str = Field(..., description="Тип узла данных, например, 'data_source'")
    connection_type: str = Field(..., description="Тип подключения, например, 'SQL', 'NoSQL', 'Streaming'")
    subtype: Optional[str] = Field(None, description="Подтип подключения, например, 'Kafka' для Streaming")
    host: str = Field(..., description="Хост для подключения")
    port: Optional[int] = Field(None, description="Порт для подключения")
    database: Optional[str] = Field(None, description="Имя базы данных")
    file_path: Optional[str] = Field(None, description="Путь к файлу, если используется File")
    credentials: Optional[Dict[str, str]] = Field(
        None,
        description="Учетные данные для подключения в формате {username: str, password: str}",
    )
    test_connection: bool = Field(..., description="Флаг проверки подключения")

    class Config:
        schema_extra = {
            "example": {
                "id": "123",
                "base_node_type": "general",
                "label": "Source Node",
                "inputs": ["node1", "node2"],
                "outputs": ["node3"],
                "data_source_type": "data_source",
                "connection_type": "SQL",
                "subtype": "PostgreSQL",
                "host": "localhost",
                "port": 5432,
                "database": "example_db",
                "file_path": None,
                "credentials": {"username": "user", "password": "pass"},
                "test_connection": True,
            }
        }


class ModelNodeBase(BaseNodeBase):
    model_node_type: str = Field("model", description="Тип модельного узла")
    environment: str = Field(..., description="Окружение модели (dev, staging, prod)")
    model_id: str = Field(..., description="Идентификатор модели")
    auth_token: Optional[str] = Field(None, description="Токен аутентификации для модели")
    timeout: Optional[int] = Field(None, description="Таймаут выполнения в секундах")


class ModelNodeCreate(BaseModel):
    label: str = Field(..., description="Название базового узла")
    inputs: Optional[Dict[str, List[str]]] = Field(None, description="Входные данные узла")
    outputs: Optional[Dict[str, List[str]]] = Field(None, description="Выходные данные узла")
    base_node_type: str = Field(..., description="Тип базового узла")

    model_node_type: str = Field(..., description="Тип узла")
    environment: str = Field(..., description="Окружение модели (например, dev, staging, prod)")
    model_id: str = Field(..., description="Идентификатор модели")
