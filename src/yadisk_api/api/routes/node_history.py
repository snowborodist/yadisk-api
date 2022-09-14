from datetime import datetime
from fastapi import APIRouter, Depends, Response

from ...services.items_service import ItemsService
from ...api.schema import SystemItemHistoryResponse
from ...utils.exception_handling import InvalidDataError

router = APIRouter(prefix="/node")


# noinspection PyPep8Naming
@router.get("/{item_id}/history", response_model=SystemItemHistoryResponse)
async def get_item_history(
        item_id: str,
        dateStart: datetime | None = None,
        dateEnd: datetime | None = None,
        service: ItemsService = Depends()) -> SystemItemHistoryResponse:
    if not dateStart and not dateEnd:
        return await service.get_item_history(item_id)
    if dateStart and dateEnd:
        return await service.get_item_history(item_id, dateStart, dateEnd)
    raise InvalidDataError("dateStart and dateEnd: none or both of the parameters must be present")
