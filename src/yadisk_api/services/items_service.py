from asyncio import gather
from datetime import datetime, timedelta
from sqlalchemy.orm.session import make_transient

from src.yadisk_api.api import schema as api
from src.yadisk_api.services.base import BaseService
from src.yadisk_api.db.repository import Repository
from src.yadisk_api.utils.type_conversion import ApiTypesFactory


class ItemsService(BaseService):
    async def get_item_info(self, system_item_id: str) -> api.SystemItem:
        async with self.session.begin():
            repo = Repository(self.session)
            await repo.validate_item_exists(system_item_id)
            root_db_item, *child_db_items = await repo.get_item_adjacency_list(system_item_id)
            return ApiTypesFactory.system_item_from_adj_list(root_db_item, child_db_items)

    async def delete_item(self, system_item_id: str, date: datetime):
        async with self.session.begin():
            repo = Repository(self.session)
            await repo.validate_item_exists(system_item_id)
            adj_list = await repo.get_item_adjacency_list(system_item_id)
            deleted_items_list = []
            for item in adj_list:
                self.session.expunge(item)
                make_transient(item)
                item.date = date
                item.deleted = True
                deleted_items_list.append(item)
            await repo.insert_items(deleted_items_list)

    async def get_file_updates(self, date: datetime) -> api.SystemItemHistoryResponse:
        async with self.session.begin():
            repo = Repository(self.session)
            date_start = date - timedelta(days=1)
            return ApiTypesFactory.history_response(
                await repo.get_file_updates(date_start, date))

    async def get_item_history(
            self, system_item_id: str,
            date_start: datetime | None = None,
            date_end: datetime | None = None) -> api.SystemItemHistoryResponse:
        async with self.session.begin():
            repo = Repository(self.session)
            await repo.validate_item_exists(system_item_id, date_end)
            dates = await repo.get_history_points_for_item(system_item_id, date_start, date_end)
            history_adj_lists = list(
                await gather(
                    *[repo.get_item_adjacency_list(
                        system_item_id, date
                    ) for date, *_ in dates]
                )
            )
            history_units = [ApiTypesFactory.system_item_from_adj_list(parent, children).history_unit
                             for parent, *children in history_adj_lists]
            return api.SystemItemHistoryResponse(items=history_units)
