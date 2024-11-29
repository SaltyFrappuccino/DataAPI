from fastapi import APIRouter

from backend.app.routes.nodes_router.nodes import nodes_router


router = APIRouter()
router.include_router(nodes_router)

__all__ = ["router"]
