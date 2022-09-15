from datetime import datetime
from fastapi import APIRouter, Depends

from ...api.schema import SystemItemHistoryResponse
from ...services.items_service import ItemsService
from . import bad_request_response

router = APIRouter(prefix="/updates")


@router.get("", response_model=SystemItemHistoryResponse, responses=bad_request_response)
async def get_item_updates(
        date: datetime,
        service: ItemsService = Depends()) -> SystemItemHistoryResponse:
    return await service.get_file_updates(date.replace(tzinfo=None))
