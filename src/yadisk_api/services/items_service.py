from ..api.schema import SystemItem, SystemItemHistoryResponse
from ..services.base import BaseService
from ..db.repositories.SystemItemRepository import SystemItemRepository


class ItemsService(BaseService):
    async def get_item_info(self, system_item_id: str) -> SystemItem | None:
        async with self.session.begin():
            repo = SystemItemRepository(self.session)
            return await repo.get_item_info(system_item_id)

    async def delete_item(self, system_item_id: str):
        async with self.session.begin():
            repo = SystemItemRepository(self.session)
            await repo.delete(system_item_id)

    async def get_item_updates(self, system_item_id: str) -> SystemItemHistoryResponse | None:
        async with self.session.begin():
            repo = SystemItemRepository(self.session)
            return await repo.get_item_updates(system_item_id)
