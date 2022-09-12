from fastapi import APIRouter

from .imports import router as imports_router
from .nodes import router as nodes_router
from .delete import router as delete_router
from .updates import router as updates_router

router = APIRouter()
router.include_router(imports_router)
router.include_router(nodes_router)
router.include_router(delete_router)
router.include_router(updates_router)
