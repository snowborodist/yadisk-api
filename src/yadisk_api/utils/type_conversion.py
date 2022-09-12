from datetime import datetime

from ..api import schema as api
from ..db import model as db


class DbTypesFactory:
    @staticmethod
    def system_item(item_import: api.SystemItemImport, date: datetime) \
            -> (db.SystemItem, db.SystemItemUpdate):
        item = db.SystemItem(
            id=item_import.id,
            type=item_import.type
        )
        update = db.SystemItemUpdate(
            item_id=item_import.id,
            parent_id=item_import.parentId,
            date=date.replace(tzinfo=None),
            url=item_import.url,
            size=item_import.size
        )
        return item, update

    @classmethod
    def system_items(cls, import_request: api.SystemItemImportRequest) \
            -> (list[db.SystemItem], list[db.SystemItemUpdate]):
        items = []
        updates = []
        for item_import in import_request.items:
            item, update = cls.system_item(
                item_import,
                import_request.updateDate)
            items.append(item)
            updates.append(update)
        return items, updates


class ApiTypesFactory:
    @staticmethod
    def history_unit(item: db.SystemItem, update: db.SystemItemUpdate) -> api.SystemItemHistoryUnit:
        return api.SystemItemHistoryUnit(
            id=item.id,
            type=item.type,
            url=update.url,
            parentId=update.parent_id,
            size=update.size,
            date=update.date
        )

    @classmethod
    def history_response(
            cls, items_updates: list[db.ItemWithUpdate]) -> api.SystemItemHistoryResponse:
        return api.SystemItemHistoryResponse(
            items=[cls.history_unit(item, update)
                   for item, update in items_updates]
        )

    @classmethod
    def system_item(cls, root_item_update: db.ItemWithUpdate,
                    child_item_updates: list[db.ItemWithUpdate]) -> api.SystemItem:
        # Define aux function
        def _pair_to_item_without_children(item_pair: db.ItemWithUpdate) -> api.SystemItem:
            h_unit = cls.history_unit(item_pair.item, item_pair.update)
            return api.SystemItem(**h_unit.dict(), children=list())

        # Cast db.ItemWithUpdate pairs to api SystemItem instances
        root_item = _pair_to_item_without_children(root_item_update)
        items = dict()
        for pair in child_item_updates:
            if not (item := items.get(pair.update.parent_id)):
                items[pair.update.parent_id] = item = list()
            item.append(_pair_to_item_without_children(pair))

        # Use BFS to construct the item tree
        not_placed_items = [root_item]
        while not_placed_items:
            current_item = not_placed_items.pop()
            children = items.get(current_item.id, list())
            not_placed_items.extend(children)
            current_item.children.extend(children)

        return root_item
