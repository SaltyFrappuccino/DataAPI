from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import and_
from typing import List


from backend.app.models import MLModel
from backend.app.routes.ml_model_router.models import *

ml_models_router = APIRouter()
ml_models_tags = ["ml_models_router"]


@cbv(ml_models_router)
class MLModelsRouter:
    def __init__(self, engine):
        self.engine = engine

    @ml_models_router.get(
        "/ml_models/",
        name="ml_models",
        response_model=List[MLModelResponse],
        description="Получает список ML-моделей из базы данных.",
        tags=ml_models_tags
    )
    async def get(
        self,
        request: Request,
        response: Response,
        params: MLModelParams = Depends()
    ):
        conditions = self.make_conditions(params)
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            if conditions:
                query = select(MLModel).filter(conditions)
            else:
                query = select(MLModel)
            result = await session.execute(query)

            data: list = [
                self.get_data_by_response_created(ml_model) for ml_model in result.scalars().all()
            ]
            if not data:
                raise HTTPException(status_code=400, detail="Ошибка при получении ML-модели.")
            result = self.get_data(data)
            return result

    @staticmethod
    def make_conditions(params: MLModelParams):
        conditions = []
        if params.name:
            conditions.append(MLModel.name == params.name)
        if params.version:
            conditions.append(MLModel.version == params.version)
        return and_(*conditions) if conditions else None

    @ml_models_router.post(
        "/ml_models/",
        name="create_ml_model",
        response_model=MLModelResponse,
        description="Создаёт новую ML-модель в базе данных.",
        tags=ml_models_tags
    )
    async def create(self, request: Request, response: Response, body: MLModelCreate):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            try:
                new_ml_model = MLModel(
                    name=body.name,
                    description=body.description,
                    version=body.version
                )
                session.add(new_ml_model)
                await session.flush()

                result = self.get_data_by_response_created(new_ml_model)

                await session.commit()
                return result
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=400, detail="Ошибка при создании ML-модели.")

    @staticmethod
    def get_data_by_response_created(ml_model: MLModel) -> dict:
        return {
            'id': ml_model.id,
            'name': ml_model.name,
            'description': ml_model.description,
            'version': ml_model.version,
        }
