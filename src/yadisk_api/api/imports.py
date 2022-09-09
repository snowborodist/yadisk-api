from fastapi import APIRouter, Depends

from ..services.imports import ImportsService
from .schema import SystemItemImportRequest

router = APIRouter(prefix="/imports")


@router.post("/")
async def post_imports(
        imports: SystemItemImportRequest,
        service: ImportsService = Depends()):
    await service.foo()
    print(imports.dict())
    return 200
