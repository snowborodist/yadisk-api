from asyncio import gather
from datetime import datetime, timedelta

from ..api.schema import SystemItem, SystemItemHistoryResponse
from ..services.base import BaseService
from ..db.repository import Repository, ItemNotFoundError

from ..utils.type_conversion import ApiTypesFactory


class ItemsService(BaseService):
    async def get_item_info(self, system_item_id: str) -> SystemItem:
        async with self.session.begin():
            repo = Repository(self.session)
            items = await repo.get_item_adjacency_list(system_item_id)
            if not items:
                raise ItemNotFoundError
            root_db_item, *child_db_items = items
            return ApiTypesFactory.system_item(root_db_item, child_db_items)

    async def delete_item(self, system_item_id: str, date: datetime):
        async with self.session.begin():
            repo = Repository(self.session)
            # adj_list = repo.get_item_adjacency_list(system_item_id)
            # for item in adj_list:
            #
            await repo.delete(system_item_id, date)

    async def get_file_updates(self, date: datetime) -> SystemItemHistoryResponse:
        async with self.session.begin():
            repo = Repository(self.session)
            date_start = date - timedelta(days=1)
            return ApiTypesFactory.history_response(
                await repo.get_file_updates(date_start, date))

    async def get_item_history(
            self, system_item_id: str,
            date_start: datetime | None = None,
            date_end: datetime | None = None) -> SystemItemHistoryResponse:
        async with self.session.begin():
            repo = Repository(self.session)
            await repo.validate_item_exists(system_item_id)
            # Get date points, when the item's subtree was changed
            dates = await repo.get_history_points_for_item(system_item_id, date_start, date_end)
            # For each date get an adjacency list of nodes
            history_adj_lists = list(
                await gather(
                    *[repo.get_item_adjacency_list(
                        system_item_id, date
                    ) for date, *_ in dates]
                )
            )
            # Assemble trees from the adjacency lists and get history unit fields
            history_units = [ApiTypesFactory.system_item(parent, children).history_unit
                             for parent, *children in history_adj_lists]
            return SystemItemHistoryResponse(items=history_units)
