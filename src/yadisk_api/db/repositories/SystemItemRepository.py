from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from .BaseRepository import BaseRepository
from ...db import model as db
from ...api import schema as api
from ...utils.type_conversion import DbTypesFactory


class SystemItemRepository(BaseRepository):
    async def validate_parent_ids(self, parent_ids: list[str]):
        # noinspection PyUnresolvedReferences
        results = await self.session.execute(
            select(db.SystemItem).filter(db.SystemItem.type == db.SystemItemType.FILE,
                                         db.SystemItem.id.in_(parent_ids))
        )
        for _ in results:
            raise ValueError("Imported items contain parent links to items of type 'FILE'")

    async def insert_imports(self, imports: api.SystemItemImportRequest):
        items, updates = DbTypesFactory.system_items(imports)
        await self._upsert_items(items)
        await self._insert_item_updates(updates)

    async def get_item_info(self, system_item_id: str) -> api.SystemItem:
        def _row_to_item(result_row) -> api.SystemItem:
            return api.SystemItem(id=result_row[0], type=result_row[1], url=result_row[2], parentId=result_row[3],
                                  size=result_row[4], date=result_row[5], children=list())

        # Use WITH RECURSIVE option available for PostgreSQL
        stmt = """
        WITH RECURSIVE r AS (
            SELECT item_id as id, type, url, parent_id as parentId, size, date
                FROM item_updates
                JOIN system_items si on item_updates.item_id = si.id
                WHERE item_id = :item_id
            
            UNION
            
            SELECT item_updates.item_id as id, system_items.type, item_updates.url, item_updates.parent_id as parentId, 
                   item_updates.size, item_updates.date
                FROM item_updates
                JOIN system_items ON item_updates.item_id = system_items.id
                JOIN r
                    ON item_updates.parent_id = r.id
        )
        
        SELECT * FROM r;
        """
        root_row, *rows = await self.session.execute(stmt, {"item_id": system_item_id})
        root_item = _row_to_item(root_row)
        other_items = dict()
        for row in rows:
            if not (item := other_items.get(row[3])):
                other_items[row[3]] = item = list()
            item.append(_row_to_item(row))

        # Use BFS to construct item tree
        not_placed_items = [root_item]
        while not_placed_items:
            current_item = not_placed_items.pop()
            children = other_items.get(current_item.id, list())
            not_placed_items.extend(children)
            current_item.children.extend(children)
        return root_item

    async def delete(self, system_item_id: str):
        stmt = delete(db.SystemItem).where(db.SystemItem.id == system_item_id)
        await self.session.execute(stmt)

    async def get_item_updates(self, system_item_id: str) -> api.SystemItemHistoryResponse:
        pass

    async def _upsert_items(self, items: list[db.SystemItem]):
        values = [{"id": item.id, "type": item.type} for item in items]
        # Use ON CONFLICT option available for PostgreSQL
        stmt = pg_insert(db.SystemItem).values(values).on_conflict_do_nothing()
        _ = await self.session.execute(stmt)

    async def _insert_item_updates(self, item_updates: list[db.SystemItemUpdate]):
        self.session.add_all(item_updates)
