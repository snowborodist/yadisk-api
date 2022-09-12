from datetime import datetime, timedelta

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

    async def get_file_updates(self, date: datetime) -> SystemItemHistoryResponse | None:
        async with self.session.begin():
            repo = SystemItemRepository(self.session)
            date_start = date - timedelta(days=1)
            return await repo.get_file_updates(date_start, date)

    async def get_item_history(
            self, system_item_id: str,
            date_start: datetime, date_end: datetime) -> SystemItemHistoryResponse | None:
        async with self.session.begin():
            repo = SystemItemRepository(self.session)
            return await repo.get_item_history(system_item_id, date_start, date_end)
