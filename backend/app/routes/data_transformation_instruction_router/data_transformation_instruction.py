from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import and_
from typing import List

from backend.app.models import DataTransformationInstruction
from backend.app.routes.data_transformation_instruction_router.models import *

data_transformation_instruction_router = APIRouter()
data_transformation_instruction_tags = ["data_transformation_instruction_router"]


@cbv(data_transformation_instruction_router)
class DataTransformationInstructionRouter:
    def __init__(self, engine):
        self.engine = engine

    @data_transformation_instruction_router.get(
        "/data_transformation_instructions/",
        name="data_transformation_instructions",
        response_model=List[DataTransformationInstructionResponse],
        description="Получает список инструкций по преобразованию данных из базы данных.",
        tags=data_transformation_instruction_tags
    )
    async def get(
        self,
        request: Request,
        response: Response,
        params: DataTransformationInstructionParams = Depends()
    ):
        conditions = self.make_conditions(params)
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            if conditions:
                query = select(DataTransformationInstruction).filter(conditions)
            else:
                query = select(DataTransformationInstruction)
            result = await session.execute(query)

            data: list = [
                self.get_data_by_response_created(instruction) for instruction in result.scalars().all()
            ]
            if not data:
                raise HTTPException(status_code=400, detail="Инструкции не найдены.")
            result = self.get_data(data)
            return result

    @staticmethod
    def make_conditions(params: DataTransformationInstructionParams):
        conditions = []
        if params.name:
            conditions.append(DataTransformationInstruction.name == params.name)
        return and_(*conditions) if conditions else None

    @data_transformation_instruction_router.post(
        "/data_transformation_instructions/",
        name="create_data_transformation_instruction",
        response_model=DataTransformationInstructionResponse,
        description="Создаёт новую инструкцию по преобразованию данных в базе данных.",
        tags=data_transformation_instruction_tags
    )
    async def create(self, request: Request, response: Response, body: DataTransformationInstructionCreate):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            try:
                new_instruction = DataTransformationInstruction(
                    name=body.name,
                    data=body.data
                )
                session.add(new_instruction)
                await session.flush()

                result = self.get_data_by_response_created(new_instruction)

                await session.commit()
                return result
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=400, detail="Ошибка при создании инструкции.")

    @staticmethod
    def get_data_by_response_created(instruction: DataTransformationInstruction) -> dict:
        return {
            'id': instruction.id,
            'name': instruction.name,
            'data': instruction.data,
        }
