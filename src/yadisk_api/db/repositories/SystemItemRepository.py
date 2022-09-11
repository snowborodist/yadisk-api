from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from .BaseRepository import BaseRepository
from ...db.model import SystemItem, SystemItemUpdate, SystemItemType


class SystemItemRepository(BaseRepository):
    async def validate_parent_ids(self, parent_ids: list[str]):
        # noinspection PyUnresolvedReferences
        results = await self.session.execute(
            select(SystemItem).filter(SystemItem.type == SystemItemType.FILE,
                                      SystemItem.id.in_(parent_ids))
        )
        for _ in results:
            raise ValueError("Imported items contain parent links to items of type 'FILE'")

    # async def get_existing_item_ids(self, item_ids: list[str]) -> set[str]:
    #     # noinspection PyUnresolvedReferences
    #     results = await self.session.execute(
    #         select(SystemItem.id).filter(SystemItem.id.in_(item_ids))
    #     )
    #     return set([item_id for item_id, *_ in results])

    async def upsert_items(self, items: list[SystemItem]):
        values = [{"id": item.id, "type": item.type} for item in items]
        stmt = pg_insert(SystemItem).values(values).on_conflict_do_nothing()
        _ = await self.session.execute(stmt)
        # self.session.add_all(items)

    async def insert_item_updates(self, item_updates: list[SystemItemUpdate]):
        self.session.add_all(item_updates)

    async def get_item(self, system_item_id: str) -> SystemItem | None:
        pass

    async def get_item_update(self, system_item_id: str, due_date: datetime) -> SystemItemUpdate | None:
        pass

    async def delete(self, system_item_id: str):
        pass
