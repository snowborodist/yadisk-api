from datetime import datetime
from fastapi import APIRouter, Depends

from ..services.items_service import ItemsService
from ..api.schema import SystemItemHistoryResponse

router = APIRouter(prefix="/node")


# noinspection PyPep8Naming
@router.get("/{item_id}/history")
async def get_item_history(
        item_id: str,
        dateStart: datetime, dateEnd: datetime,
        service: ItemsService = Depends()) -> SystemItemHistoryResponse | None:
    return await service.get_item_history(item_id, dateStart, dateEnd)
