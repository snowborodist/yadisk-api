from fastapi import APIRouter, Depends

from ...services.items_service import ItemsService

router = APIRouter(prefix="/delete")


@router.delete("/{item_id}")
async def delete_item(item_id: str, service: ItemsService = Depends()):
    await service.delete_item(item_id)
    return
