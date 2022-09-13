from datetime import datetime
from fastapi import APIRouter, Depends

from ...services.items_service import ItemsService
from ...api.schema import SystemItemHistoryResponse

router = APIRouter(prefix="/node")


# noinspection PyPep8Naming
@router.get("/{item_id}/history")
async def get_item_history(
        item_id: str,
        dateStart: datetime | None = None,
        dateEnd: datetime | None = None,
        service: ItemsService = Depends()) -> SystemItemHistoryResponse | None:
    if not dateStart and not dateEnd:
        return await service.get_item_history(item_id)
    if dateStart and dateEnd:
        return await service.get_item_history(
            system_item_id=item_id,
            date_start=dateStart.replace(tzinfo=None),
            date_end=dateEnd.replace(tzinfo=None))
    raise ValueError("dateStart and dateEnd:  none or both of the parameters must be present")
