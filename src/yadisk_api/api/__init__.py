from fastapi import APIRouter

from .routes.imports import router as imports_router
from .routes.nodes import router as nodes_router
from .routes.delete import router as delete_router
from .routes.updates import router as updates_router

router = APIRouter()
router.include_router(imports_router)
router.include_router(nodes_router)
router.include_router(delete_router)
router.include_router(updates_router)
