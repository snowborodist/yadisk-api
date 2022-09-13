from datetime import datetime
from sqlalchemy import delete, and_, update
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

    async def insert_items(self, items: list[db.SystemItem]):
        await self._validate_item_types(items)
        await self._insert_items(items)
        await self._insert_items_links(items)

    async def _validate_item_types(self, items: list[db.SystemItem]):
        rows = [dict(system_item_id=item.id, system_item_type=item.type) for item in items]
        stmt = pg_insert(db.SystemItemTypeMatch).values(rows)
        stmt = stmt.on_conflict_do_update(index_elements=[db.SystemItemTypeMatch.system_item_id],
                                          set_=dict(system_item_type=stmt.excluded.system_item_type))
        await self.session.execute(stmt)

    async def _insert_items(self, items: list[db.SystemItem]):
        self.session.add_all(items)

    async def _insert_items_links(self, items: list[db.SystemItem]):
        for item in items:
            loop_link = db.SystemItemLink(parent_id=item.id, child_id=item.id, date=item.date, depth=0)
            self.session.add(loop_link)
            if parent_id := item.parent_id:
                await self._link_children(parent_id, item.id, item.date)

    async def _link_children(self, parent_id: str, child_id: str, date: datetime):
        stmt = """
        INSERT INTO system_item_links(parent_id, child_id, date, depth)
            SELECT p.parent_id, c.child_id, :date, p.depth + c.depth + 1
            FROM system_item_links p, system_item_links c
            WHERE p.child_id = :parent_id AND c.parent_id = :child_id;
        """
        await self.session.execute(stmt, dict(date=date, parent_id=parent_id, child_id=child_id))

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
