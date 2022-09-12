from datetime import datetime
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert

from . import model as db


class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def validate_parent_ids(self, parent_ids: list[str]):
        # noinspection PyUnresolvedReferences
        results = await self.session.execute(
            select(db.SystemItem).filter(db.SystemItem.type == db.SystemItemType.FILE,
                                         db.SystemItem.id.in_(parent_ids))
        )
        for _ in results:
            raise ValueError("Imported items contain parent links to items of type 'FILE'")

    async def upsert_items(self, items: list[db.SystemItem]):
        values = [{"id": item.id, "type": item.type} for item in items]
        # Use ON CONFLICT option available for PostgreSQL
        stmt = pg_insert(db.SystemItem).values(values).on_conflict_do_nothing()
        _ = await self.session.execute(stmt)

    async def insert_item_updates(self, item_updates: list[db.SystemItemUpdate]):
        self.session.add_all(item_updates)

    async def get_item_info(self, system_item_id: str) -> list[db.ItemWithUpdate]:
        def _row_to_item_and_update(result_row) -> db.ItemWithUpdate:
            return db.ItemWithUpdate(
                db.SystemItem(id=result_row[2],
                              type=result_row[3]),
                db.SystemItemUpdate(id=result_row[1],
                                    item_id=result_row[2],
                                    parent_id=result_row[5],
                                    date=result_row[7],
                                    url=result_row[4],
                                    size=result_row[6])
            )

        # Use WITH RECURSIVE option available for PostgreSQL
        stmt = """
        WITH RECURSIVE r AS (
            (SELECT DISTINCT ON (si.id) si.id, item_updates.id as update_id, item_id, type, url, parent_id, size, date
                FROM item_updates
                JOIN system_items si on item_updates.item_id = si.id
                WHERE item_id = :item_id
                ORDER BY si.id, item_updates.date DESC)
            UNION

            (SELECT DISTINCT ON (system_items.id) system_items.id, item_updates.id as update_id, item_updates.item_id,
                   system_items.type, item_updates.url, item_updates.parent_id,
                   item_updates.size, item_updates.date
                FROM item_updates
                JOIN system_items ON item_updates.item_id = system_items.id
                JOIN r ON item_updates.parent_id = r.id
                ORDER BY system_items.id, item_updates.date DESC)
        )
        SELECT * FROM r;
        """
        return [_row_to_item_and_update(row) for row in
                await self.session.execute(stmt, {"item_id": system_item_id})]

    async def delete(self, system_item_id: str):
        stmt = delete(db.SystemItem).where(db.SystemItem.id == system_item_id)
        await self.session.execute(stmt)

    async def get_file_updates(
            self, date_start: datetime, date_end: datetime) -> list[db.ItemWithUpdate]:
        # noinspection PyUnresolvedReferences
        stmt = select(db.SystemItem, db.SystemItemUpdate) \
            .join(db.SystemItem, db.SystemItemUpdate.item_id == db.SystemItem.id) \
            .filter(db.SystemItem.type == db.SystemItemType.FILE,
                    db.SystemItemUpdate.date.between(date_start, date_end))
        rows = await self.session.execute(stmt)
        return [db.ItemWithUpdate(item, update) for item, update in rows]

    async def get_item_history(
            self, system_item_id: str,
            date_start: datetime, date_end: datetime) -> list[db.ItemWithUpdate]:
        raise NotImplementedError
