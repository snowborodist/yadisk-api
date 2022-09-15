from fastapi import APIRouter, Depends

from src.yadisk_api.services.imports_service import ImportsService
from src.yadisk_api.api.schema import SystemItemImportRequest
from src.yadisk_api.api.routes import bad_request_response

router = APIRouter(prefix="/imports")


@router.post("", responses=bad_request_response)
async def post_imports(
        imports: SystemItemImportRequest,
        service: ImportsService = Depends()):
    await service.emplace_imports(imports)
    return
