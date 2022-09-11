from fastapi import APIRouter

from .imports import router as imports_router
from .nodes import router as nodes_router

router = APIRouter()
router.include_router(imports_router)
router.include_router(nodes_router)
