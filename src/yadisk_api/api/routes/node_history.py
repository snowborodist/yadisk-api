from datetime import datetime
from fastapi import APIRouter, Depends

from ...services.items_service import ItemsService
from ...api.schema import SystemItemHistoryResponse

router = APIRouter(prefix="/node")


# noinspection PyPep8Naming
@router.get("/{item_id}/history", response_model=SystemItemHistoryResponse)
async def get_item_history(
        item_id: str,
        dateStart: datetime | None = None,
        dateEnd: datetime | None = None,
        service: ItemsService = Depends()) -> SystemItemHistoryResponse:
    if dateStart:
        dateStart = dateStart.replace(tzinfo=None)
    if dateEnd:
        dateEnd = dateEnd.replace(tzinfo=None)
    return await service.get_item_history(item_id, dateStart, dateEnd)
