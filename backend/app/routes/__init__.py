from fastapi import APIRouter

from backend.app.routes.artifact_router.artifact import artifact_router
from backend.app.routes.contract_router.contracts import contracts_router
from backend.app.routes.data_transformation_instruction_router.data_transformation_instruction import \
    data_transformation_instruction_router
from backend.app.routes.db_connection_router.db_connections import db_connection_router
from backend.app.routes.log_router.logs import log_router
from backend.app.routes.ml_model_router.ml_models import ml_models_router
from backend.app.routes.nodes_router.nodes import nodes_router


router = APIRouter()
router.include_router(ml_models_router)
router.include_router(contracts_router)
router.include_router(db_connection_router)
router.include_router(data_transformation_instruction_router)
router.include_router(artifact_router)
router.include_router(log_router)

router.include_router(nodes_router)

__all__ = ["router"]
