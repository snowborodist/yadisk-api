from fastapi import APIRouter, Depends

from ...api.schema import SystemItem
from ...services.items_service import ItemsService

router = APIRouter(prefix="/nodes")


@router.get("/{item_id}", response_model=SystemItem)
async def get_system_item(
        item_id: str,
        service: ItemsService = Depends()) -> SystemItem:
    return await service.get_item_info(item_id)
