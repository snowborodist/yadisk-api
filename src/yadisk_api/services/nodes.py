from ..api.schema import SystemItem
from ..services.base import BaseService
from ..db.repositories.SystemItemRepository import SystemItemRepository


class NodeServices(BaseService):
    async def get_item_info(self, system_item_id: str) -> SystemItem | None:
        async with self.session.begin():
            repo = SystemItemRepository(self.session)
            return await repo.get_item_info(system_item_id)
