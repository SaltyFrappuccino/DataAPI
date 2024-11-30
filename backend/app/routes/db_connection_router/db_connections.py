from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import and_
from typing import List

from backend.app.models import DBConnection
from backend.app.routes.db_connection_router.models import *

db_connection_router = APIRouter()
db_connection_tags = ["db_connection_router"]


@cbv(db_connection_router)
class DBConnectionRouter:
    def __init__(self, engine):
        self.engine = engine

    @db_connection_router.get(
        "/db_connections/",
        name="db_connections",
        response_model=List[DBConnectionResponse],
        description="Получает список подключений к базе данных.",
        tags=db_connection_tags
    )
    async def get(
        self,
        request: Request,
        response: Response,
        params: DBConnectionParams = Depends()
    ):
        conditions = self.make_conditions(params)
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            if conditions:
                query = select(DBConnection).filter(conditions)
            else:
                query = select(DBConnection)
            result = await session.execute(query)

            data: list = [
                self.get_data_by_response_created(connection) for connection in result.scalars().all()
            ]
            if not data:
                raise HTTPException(status_code=400, detail="Ошибка при получении подключений к базе данных.")
            result = self.get_data(data)
            return result

    @staticmethod
    def make_conditions(params: DBConnectionParams):
        conditions = []
        if params.name:
            conditions.append(DBConnection.name == params.name)
        if params.db_type:
            conditions.append(DBConnection.db_type == params.db_type)
        return and_(*conditions) if conditions else None

    @db_connection_router.post(
        "/db_connections/",
        name="create_db_connection",
        response_model=DBConnectionResponse,
        description="Создаёт новое подключение к базе данных.",
        tags=db_connection_tags
    )
    async def create(self, request: Request, response: Response, body: DBConnectionCreate):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            try:
                new_db_connection = DBConnection(
                    name=body.name,
                    db_type=body.db_type,
                    host=body.host,
                    port=body.port,
                    database=body.database,
                    username=body.username,
                    password=body.password
                )
                session.add(new_db_connection)
                await session.flush()

                result = self.get_data_by_response_created(new_db_connection)

                await session.commit()
                return result
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=400, detail="Ошибка при создании подключения к базе данных.")

    @staticmethod
    def get_data_by_response_created(connection: DBConnection) -> dict:
        return {
            'id': connection.id,
            'name': connection.name,
            'db_type': connection.db_type,
            'host': connection.host,
            'port': connection.port,
            'database': connection.database,
            'username': connection.username,
            'password': connection.password,
        }
