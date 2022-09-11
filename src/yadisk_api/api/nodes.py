from fastapi import APIRouter, Depends

from ..services.nodes import NodeServices

router = APIRouter(prefix="/nodes")


@router.get("/{item_id}")
async def get_system_item(
        item_id: str,
        service: NodeServices = Depends()):
    node = await service.get_item_info(item_id)
    return node
