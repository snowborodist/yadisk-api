from fastapi import APIRouter

from .imports import router as imports_router

router = APIRouter()
router.include_router(imports_router)
