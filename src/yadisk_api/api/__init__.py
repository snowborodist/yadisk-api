from fastapi import APIRouter

from src.yadisk_api.api.routes.imports import router as imports_router
from src.yadisk_api.api.routes.nodes import router as nodes_router
from src.yadisk_api.api.routes.delete import router as delete_router
from src.yadisk_api.api.routes.updates import router as updates_router
from src.yadisk_api.api.routes.node_history import router as history_router

router = APIRouter()
router.include_router(imports_router)
router.include_router(nodes_router)
router.include_router(delete_router)
router.include_router(updates_router)
router.include_router(history_router)
