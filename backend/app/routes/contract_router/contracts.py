from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi_utils.cbv import cbv
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import and_
from typing import List

from backend.app.models import Contract
from backend.app.routes.contract_router.models import *

contracts_router = APIRouter()
contracts_tags = ["contracts_router"]


@cbv(contracts_router)
class ContractsRouter:
    def __init__(self, engine):
        self.engine = engine

    @contracts_router.get(
        "/contracts/",
        name="contracts",
        response_model=List[ContractResponse],
        description="Получает список контрактов из базы данных.",
        tags=contracts_tags
    )
    async def get(
        self,
        request: Request,
        response: Response,
        params: ContractParams = Depends()
    ):
        conditions = self.make_conditions(params)
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            if conditions:
                query = select(Contract).filter(conditions)
            else:
                query = select(Contract)
            result = await session.execute(query)

            data: list = [
                self.get_data_by_response_created(contract) for contract in result.scalars().all()
            ]
            if not data:
                raise HTTPException(status_code=400, detail="Ошибка при получении контракта.")
            result = self.get_data(data)
            return result

    @staticmethod
    def make_conditions(params: ContractParams):
        conditions = []
        if params.name:
            conditions.append(Contract.name == params.name)
        if params.description:
            conditions.append(Contract.description.like(f"%{params.description}%"))
        return and_(*conditions) if conditions else None

    @contracts_router.post(
        "/contracts/",
        name="create_contract",
        response_model=ContractResponse,
        description="Создаёт новый контракт в базе данных.",
        tags=contracts_tags
    )
    async def create(self, request: Request, response: Response, body: ContractCreate):
        async with AsyncSession(self.engine, autoflush=False, expire_on_commit=False) as session:
            try:
                new_contract = Contract(
                    name=body.name,
                    description=body.description,
                    data=body.data
                )
                session.add(new_contract)
                await session.flush()

                result = self.get_data_by_response_created(new_contract)

                await session.commit()
                return result
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=400, detail="Ошибка при создании контракта.")

    @staticmethod
    def get_data_by_response_created(contract: Contract) -> dict:
        return {
            'id': contract.id,
            'name': contract.name,
            'description': contract.description,
            'data': contract.data,
        }
