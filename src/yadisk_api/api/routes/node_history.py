from datetime import datetime
from fastapi import APIRouter, Depends

from src.yadisk_api.services.items_service import ItemsService
from src.yadisk_api.api.schema import SystemItemHistoryResponse
from src.yadisk_api.api.routes import common_responses

router = APIRouter(prefix="/node")


# noinspection PyPep8Naming
@router.get("/{item_id}/history",
            response_model=SystemItemHistoryResponse,
            responses=common_responses)
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
