from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import and_
from typing import List

from backend.app.models import Log
from backend.app.routes.log_router.models import *

log_router = APIRouter()
log_tags = ["log_router"]


@cbv(log_router)
class LogRouter:
    def __init__(self, engine):
        self.engine = engine

    @log_router.get(
        "/logs/",
        name="logs",
        response_model=List[LogResponse],
        description="Получает список логов из базы данных.",
        tags=log_tags
    )
    async def get(
        self,
        request: Request,
        response: Response,
        params: LogParams = Depends()
    ):
        conditions = self.make_conditions(params)
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            if conditions:
                query = select(Log).filter(conditions)
            else:
                query = select(Log)
            result = await session.execute(query)

            data: list = [
                self.get_data_by_response_created(log) for log in result.scalars().all()
            ]
            if not data:
                raise HTTPException(status_code=400, detail="Логи не найдены.")
            result = self.get_data(data)
            return result

    @staticmethod
    def make_conditions(params: LogParams):
        conditions = []
        if params.model_id:
            conditions.append(Log.model_id == params.model_id)
        if params.contract_id:
            conditions.append(Log.contract_id == params.contract_id)
        return and_(*conditions) if conditions else None

    @log_router.post(
        "/logs/",
        name="create_log",
        response_model=LogResponse,
        description="Создаёт новый лог в базе данных.",
        tags=log_tags
    )
    async def create(self, request: Request, response: Response, body: LogCreate):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            try:
                new_log = Log(
                    model_id=body.model_id,
                    transformation_instruction_id=body.transformation_instruction_id,
                    contract_id=body.contract_id,
                    data=body.data
                )
                session.add(new_log)
                await session.flush()

                result = self.get_data_by_response_created(new_log)

                await session.commit()
                return result
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=400, detail="Ошибка при создании лога.")

    @staticmethod
    def get_data_by_response_created(log: Log) -> dict:
        return {
            'id': log.id,
            'model_id': log.model_id,
            'transformation_instruction_id': log.transformation_instruction_id,
            'contract_id': log.contract_id,
            'data': log.data,
        }
