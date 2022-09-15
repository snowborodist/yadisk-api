from fastapi import APIRouter, Depends

from src.yadisk_api.api.schema import SystemItem
from src.yadisk_api.services.items_service import ItemsService
from src.yadisk_api.api.routes import common_responses

router = APIRouter(prefix="/nodes")


@router.get("/{item_id}",
            response_model=SystemItem,
            responses=common_responses)
async def get_system_item(
        item_id: str,
        service: ItemsService = Depends()) -> SystemItem:
    return await service.get_item_info(item_id)
