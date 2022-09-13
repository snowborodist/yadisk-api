from datetime import datetime
from sqlalchemy import delete, insert, and_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert

from . import model as db


class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def validate_item_type(self, item: db.SystemItem):
        await self.session.execute(
            pg_insert(db.SystemItemTypeMatch).values(item.id, item.type).on_conflict_do_nothing()
        )

    async def validate_parent_ids(self, parent_ids: list[str]):
        # noinspection PyUnresolvedReferences
        results = await self.session.execute(
            select(db.SystemItem).filter(db.SystemItem.type == db.SystemItemType.FILE,
                                         db.SystemItem.id.in_(parent_ids))
        )
        for _ in results:
            raise ValueError("Imported items contain parent links to items of type 'FILE'")

    async def insert_items(self, items: list[db.SystemItem]):
        for item_pair in items:
            await self._insert_item(item_pair)

    async def _insert_item(self, item: db.SystemItem):
        await self.session.execute(insert(item))
        await self._add_loop_link(item.id, item.date)
        if item.parent_id:
            await self._link_child(item.parent_id, item.id, item.date)

    async def _add_loop_link(self, item_id: str, date: datetime):
        await self.session.execute(insert(db.SystemItemLink).values(item_id, item_id, date, 0))

    async def _link_child(self, parent_id: str, child_id: str, date: datetime):
        stmt = """
        INSERT INTO system_item_links(parent_id, child_id, date, depth)
            SELECT p.parent, c.child, :date, p.depth + c.depth + 1
            FROM system_item_links p, system_item_links c
            WHERE p.child_id = :parent_id AND c.parent_id = :child_id;
        """
        await self.session.execute(stmt, date=date, parent_id=parent_id, child_id=child_id)

    async def get_item_adjacency_list(
            self, system_item_id: str, date: datetime | None = None) -> list[db.SystemItem]:
        """
        Get an adjacency list for a SystemItem with the given id.
        @param system_item_id: item_id of the adjacency list's root item.
        @param date: datetime point for the list selection.
        @return a list of named tuples of type db.ItemWithParentId (adjacency list).
        The first item in the list is the root item.
        """
        stmt = select(db.SystemItem) \
            .join(db.SystemItemLink,
                  db.SystemItem.id == db.SystemItemLink.child_id) \
            .distinct(db.SystemItem.id)
        if date:
            stmt = stmt.where(and_(db.SystemItemLink.parent_id == system_item_id,
                                   db.SystemItem.date == date))
        else:
            stmt = stmt.where(db.SystemItemLink.parent_id == system_item_id)
        stmt = stmt.order_by(db.SystemItem.id, db.SystemItem.date.desc())

        rows = await self.session.execute(stmt)
        return list(rows)

    async def delete(self, system_item_id: str):
        stmt = delete(db.SystemItem).where(db.SystemItem.id == system_item_id)
        await self.session.execute(stmt)

    async def get_file_updates(
            self, date_start: datetime, date_end: datetime) -> list[db.SystemItem]:
        # noinspection PyUnresolvedReferences
        stmt = select(db.SystemItem) \
            .filter(db.SystemItem.type == db.SystemItemType.FILE,
                    db.SystemItem.date.between(date_start, date_end))
        rows = await self.session.execute(stmt)
        return list(rows)

    async def get_item_history(
            self, system_item_id: str,
            date_start: datetime, date_end: datetime) -> list[list[db.SystemItem]]:
        # Get date points, when the item's subtree was changed
        # noinspection PyUnresolvedReferences
        stmt = select(db.SystemItemLink.date) \
            .where(and_(db.SystemItemLink.parent_id == system_item_id,
                        db.SystemItemLink.date.between(date_start, date_end)))
        dates = list(await self.session.execute(stmt))
        # For each date get an adjacency list of nodes
        result = []
        for date in dates:
            result.append(await self.get_item_adjacency_list(system_item_id, date))
        return result
