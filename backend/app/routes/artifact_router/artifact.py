from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import and_
from typing import List

from backend.app.models import Artifact
from backend.app.routes.artifact_router.models import *

artifact_router = APIRouter()
artifact_tags = ["artifact_router"]


@cbv(artifact_router)
class ArtifactRouter:
    def __init__(self, engine):
        self.engine = engine

    @artifact_router.get(
        "/artifacts/",
        name="artifacts",
        response_model=List[ArtifactResponse],
        description="Получает список артефактов из базы данных.",
        tags=artifact_tags
    )
    async def get(
        self,
        request: Request,
        response: Response,
        params: ArtifactParams = Depends()
    ):
        conditions = self.make_conditions(params)
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            if conditions:
                query = select(Artifact).filter(conditions)
            else:
                query = select(Artifact)
            result = await session.execute(query)

            data: list = [
                self.get_data_by_response_created(artifact) for artifact in result.scalars().all()
            ]
            if not data:
                raise HTTPException(status_code=400, detail="Артефакты не найдены.")
            result = self.get_data(data)
            return result

    @staticmethod
    def make_conditions(params: ArtifactParams):
        conditions = []
        if params.name:
            conditions.append(Artifact.name == params.name)
        return and_(*conditions) if conditions else None

    @artifact_router.post(
        "/artifacts/",
        name="create_artifact",
        response_model=ArtifactResponse,
        description="Создаёт новый артефакт в базе данных.",
        tags=artifact_tags
    )
    async def create(self, request: Request, response: Response, body: ArtifactCreate):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            try:
                new_artifact = Artifact(
                    name=body.name,
                    data=body.data
                )
                session.add(new_artifact)
                await session.flush()

                result = self.get_data_by_response_created(new_artifact)

                await session.commit()
                return result
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=400, detail="Ошибка при создании артефакта.")

    @staticmethod
    def get_data_by_response_created(artifact: Artifact) -> dict:
        return {
            'id': artifact.id,
            'name': artifact.name,
            'data': artifact.data,
        }
