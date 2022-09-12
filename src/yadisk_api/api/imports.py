from http import HTTPStatus
from fastapi import APIRouter, Depends

from ..services.imports_service import ImportsService
from .schema import SystemItemImportRequest

router = APIRouter(prefix="/imports")


@router.post("")
async def post_imports(
        imports: SystemItemImportRequest,
        service: ImportsService = Depends()):
    await service.emplace_imports(imports)
    return HTTPStatus.OK
