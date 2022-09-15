from fastapi import APIRouter, Depends

from ...services.imports_service import ImportsService
from ..schema import SystemItemImportRequest
from . import bad_request_response

router = APIRouter(prefix="/imports")


@router.post("", responses=bad_request_response)
async def post_imports(
        imports: SystemItemImportRequest,
        service: ImportsService = Depends()):
    await service.emplace_imports(imports)
    return
