from datetime import datetime
from fastapi import APIRouter, Depends

from src.yadisk_api.services.items_service import ItemsService
from src.yadisk_api.api.routes import common_responses

router = APIRouter(prefix="/delete")


@router.delete("/{item_id}", responses=common_responses)
async def delete_item(
        item_id: str,
        date: datetime,
        service: ItemsService = Depends()):
    await service.delete_item(item_id, date.replace(tzinfo=None))
    return
