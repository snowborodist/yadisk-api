from datetime import datetime
from fastapi import APIRouter, Depends

from ...api.schema import SystemItemHistoryResponse
from ...services.items_service import ItemsService

router = APIRouter(prefix="/updates")


@router.get("", response_model=SystemItemHistoryResponse)
async def get_item_updates(
        date: datetime,
        service: ItemsService = Depends()) -> SystemItemHistoryResponse:
    return await service.get_file_updates(date.replace(tzinfo=None))
