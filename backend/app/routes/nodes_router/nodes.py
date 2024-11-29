from fastapi import APIRouter, Request, Response, Depends
from fastapi_utils.cbv import cbv
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.config import SANIC_BASE_URL
from backend.app.models import DataSourceNode, ModelNode, BaseNode
from backend.app.orm_sender.manager_sqlalchemy import ManagerSQLAlchemy
from backend.app.routes.main import MainRouterMIXIN
from backend.app.routes.nodes_router.models import *
from backend.app.routes.nodes_router.response_models import *

import httpx
import time

nodes_router = APIRouter()
nodes_tags = ["nodes_router"]


@cbv(nodes_router)
class NodeSourceRouter(MainRouterMIXIN, ManagerSQLAlchemy):

    @nodes_router.get(
        "/node_source/",
        name='node_source',
        response_model=DataSourceResponse,
        responses=node_source_responses,
        description='Data Source Node вызывает Data Source Service,'
                    ' который подключается к источнику данных (например, PostgreSQL) '
                    'и возвращает JSON с сырыми данными.',
        tags=nodes_tags
    )
    async def get(self, request: Request, response: Response, params: NodeSourceParams = Depends()):
        conditions = self.make_conditions(params)
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            if conditions is not None:
                data_source_node_select = await session.execute(select(DataSourceNode).filter(conditions))
            else:
                data_source_node_select = await session.execute(select(DataSourceNode))
            data_sources_node = data_source_node_select.scalars().all()
            data: list = [
                self.get_data_by_response_created(data_source_node) for data_source_node in data_sources_node
            ]
            result = self.get_data(data)
            return result

    @staticmethod
    def make_conditions(params: NodeSourceParams):
        conditions: list = []

        return and_(*conditions) if conditions else None

    @staticmethod
    def get_data_by_response_created(node_source: DataSourceNode) -> dict:
        base_node = node_source.base_node
        return {
            'id': base_node.id,
            'base_node_type': base_node.base_node_type,
            'label': base_node.label,
            'inputs': base_node.inputs,
            'outputs': base_node.outputs,

            'data_source_type': node_source.data_source_type,
            'connection_type': node_source.connection_type,
            'subtype': node_source.subtype,
            'host': node_source.host,
            'port': node_source.port,
            'database': node_source.database,
            'file_path': node_source.file_path,
            'credentials': node_source.credentials,
            'test_connection': node_source.test_connection,
        }


@cbv(nodes_router)
class ModelNodeRouter(MainRouterMIXIN, ManagerSQLAlchemy):

    @nodes_router.post(
        "/model_node/",
        name='model_node',
        response_model=ModelNodeBase,
        responses=node_model_responses,
        description='Model Node вызывает Model API Service, который отправляет данные в ML-модель и получает результат.',
        tags=nodes_tags
    )
    async def post(self, request: Request, response: Response, body: ModelNodeCreate):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            base_node = BaseNode(
                base_node_type=body.base_node_type,
                label=body.label,
                inputs=body.inputs,
                outputs=body.outputs,
            )
            session.add(base_node)
            await session.flush()

            start_time = time.time()
            data_from_ml: dict = await self.send_data_to_ml()
            end_time = time.time()

            model_node: ModelNode = ModelNode(
                id=base_node.id,
                model_node_type=body.model_node_type,
                environment=body.environment,
                model_id=body.model_id,
                timeout=round(end_time - start_time, 3),
                # auth_token=body.auth_token,
            )

            session.add(model_node)
            await session.commit()

            result = self.get_data(self.get_data_by_response_created(model_node, base_node))
            return result

    @staticmethod
    async def send_data_to_ml(model_name: str = 'model_name') -> dict:
        async with httpx.AsyncClient(verify=False) as client:
            data = {'test': 'test'}
            response = await client.post(f"{SANIC_BASE_URL}/api/ml/{model_name}", json=data)
            return response.json()

    @staticmethod
    def get_data_by_response_created(model_node: ModelNode, base_node: BaseNode) -> dict:
        return {
            "id": base_node.id,
            "base_node_type": base_node.base_node_type,
            "label": base_node.label,
            "inputs": base_node.inputs,
            "outputs": base_node.outputs,

            "model_node_type": model_node.model_node_type,
            "environment": model_node.environment,
            "model_id": model_node.model_id,
            "auth_token": model_node.auth_token,
            "timeout": model_node.timeout,
        }
