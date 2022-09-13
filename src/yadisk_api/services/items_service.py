from datetime import datetime, timedelta

from ..api.schema import SystemItem, SystemItemHistoryResponse
from ..services.base import BaseService
from ..db.repository import Repository

from ..utils.type_conversion import ApiTypesFactory


class ItemsService(BaseService):
    async def get_item_info(self, system_item_id: str) -> SystemItem | None:
        async with self.session.begin():
            repo = Repository(self.session)
            root_db_item, *child_db_items = await repo.get_item_adjacency_list(system_item_id)
            return ApiTypesFactory.system_item(root_db_item, child_db_items)

    async def delete_item(self, system_item_id: str):
        async with self.session.begin():
            repo = Repository(self.session)
            await repo.delete(system_item_id)

    async def get_file_updates(self, date: datetime) -> SystemItemHistoryResponse:
        async with self.session.begin():
            repo = Repository(self.session)
            date_start = date - timedelta(days=1)
            return ApiTypesFactory.history_response(
                await repo.get_file_updates(date_start, date))

    async def get_item_history(
            self, system_item_id: str,
            date_start: datetime| None = None,
            date_end: datetime | None = None) -> SystemItemHistoryResponse:
        async with self.session.begin():
            repo = Repository(self.session)
            history_adj_lists = await repo.get_item_history(system_item_id, date_start, date_end)
            history_units = [ApiTypesFactory.system_item(parent, children).history_unit
                             for parent, *children in history_adj_lists]
            return SystemItemHistoryResponse(items=history_units)
