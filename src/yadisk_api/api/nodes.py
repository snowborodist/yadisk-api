from fastapi import APIRouter, Depends

from ..services.items_service import ItemsService

router = APIRouter(prefix="/nodes")


@router.get("/{item_id}")
async def get_system_item(
        item_id: str,
        service: ItemsService = Depends()):
    node = await service.get_item_info(item_id)
    return node
