from datetime import datetime
from sqlalchemy import delete, and_, or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert

from . import model as db


class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def validate_parent_ids(self, parent_ids: list[str]):
        # noinspection PyUnresolvedReferences
        rows = await self.session.execute(
            select(db.SystemItem).filter(db.SystemItem.type == db.SystemItemType.FILE,
                                         db.SystemItem.id.in_(parent_ids))
        )
        for _ in rows:
            raise ValueError("Imported items contain parent links to items of type 'FILE'")

    async def insert_items(self, items: list[db.SystemItem]):
        await self._validate_item_types(items)
        await self._insert_items(items)
        await self.session.flush()
        await self._insert_items_child_links(items)

    async def _validate_item_types(self, items: list[db.SystemItem]):
        rows = [dict(system_item_id=item.id, system_item_type=item.type) for item in items]
        stmt = pg_insert(db.SystemItemTypeMatch).values(rows)
        stmt = stmt.on_conflict_do_update(index_elements=[db.SystemItemTypeMatch.system_item_id],
                                          set_=dict(system_item_type=stmt.excluded.system_item_type))
        await self.session.execute(stmt)

    async def _insert_items(self, items: list[db.SystemItem]):
        self.session.add_all(items)
        loop_links = [
            db.SystemItemLink(parent_id=item.id, child_id=item.id, date=item.date, depth=0)
            for item in items
        ]
        self.session.add_all(loop_links)

    async def _insert_items_child_links(self, items: list[db.SystemItem]):
        for item in items:
            if parent_id := item.parent_id:
                await self._link_children(parent_id, item.id, item.date)

    async def _link_children(self, parent_id: str, child_id: str, date: datetime):
        stmt = """
        INSERT INTO system_item_links(parent_id, child_id, date, depth)
            SELECT DISTINCT ON (p.parent_id, c.child_id) p.parent_id, c.child_id, :date, p.depth + c.depth + 1
            FROM system_item_links p, system_item_links c
            WHERE p.child_id = :parent_id AND c.parent_id = :child_id
            ORDER BY p.parent_id, c.child_id, p.date DESC, c.date DESC
        ON CONFLICT DO NOTHING;
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
        return [row for row, *_ in rows]

    async def delete(self, system_item_id: str):
        # Get ids to delete
        item_ids_to_delete = await self._get_descendants_ids(system_item_id)
        # Delete all links
        stmt = delete(db.SystemItemLink).where(
            or_(db.SystemItemLink.parent_id.in_(item_ids_to_delete),
                db.SystemItemLink.child_id.in_(item_ids_to_delete)))
        await self.session.execute(stmt)
        # Delete type match guards
        stmt = delete(db.SystemItemTypeMatch) \
            .where(db.SystemItemTypeMatch.system_item_id.in_(item_ids_to_delete))
        await self.session.execute(stmt)
        # Delete the item and all descendants
        stmt = delete(db.SystemItem).where(db.SystemItem.id.in_(item_ids_to_delete))
        await self.session.execute(stmt)

    async def _get_descendants_ids(self, system_item_id) -> list[str]:
        stmt = select(db.SystemItem.id).distinct() \
            .join(db.SystemItemLink, db.SystemItem.id == db.SystemItemLink.child_id) \
            .where(db.SystemItemLink.parent_id == system_item_id)
        rows = await self.session.execute(stmt)
        return [row for row, *_ in rows]

    async def get_file_updates(
            self, date_start: datetime, date_end: datetime) -> list[db.SystemItem]:
        # noinspection PyUnresolvedReferences
        stmt = select(db.SystemItem) \
            .filter(db.SystemItem.type == db.SystemItemType.FILE,
                    db.SystemItem.date.between(date_start, date_end))
        rows = await self.session.execute(stmt)
        return [row for row, *_ in rows]

    async def get_item_history(
            self, system_item_id: str,
            date_start: datetime | None = None,
            date_end: datetime | None = None) -> list[list[db.SystemItem]]:
        # Get date points, when the item's subtree was changed
        stmt = select(db.SystemItemLink.date)
        if date_start and date_end:
            # noinspection PyUnresolvedReferences
            stmt = stmt.where(and_(db.SystemItemLink.parent_id == system_item_id,
                                   and_(db.SystemItemLink.date >= date_start,
                                        db.SystemItemLink.date < date_end)))
        else:
            stmt = stmt.where(db.SystemItemLink.parent_id == system_item_id)
        dates = list(await self.session.execute(stmt))
        # For each date get an adjacency list of nodes
        result = []
        for date, *_ in dates:
            result.append(await self.get_item_adjacency_list(system_item_id, date))
        return result
