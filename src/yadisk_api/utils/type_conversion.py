from datetime import datetime

from ..api import schema as api
from ..db import model as db


class DbTypesFactory:
    @staticmethod
    def system_item(item_import: api.SystemItemImport, date: datetime) -> db.SystemItem:
        return db.SystemItem(
            id=item_import.id,
            parent_id=item_import.parentId,
            date=date.replace(tzinfo=None),
            type=item_import.type,
            url=item_import.url,
            size=item_import.size
        )

    @classmethod
    def system_items(cls, import_request: api.SystemItemImportRequest) -> list[db.SystemItem]:
        return [cls.system_item(item_import, import_request.updateDate)
                for item_import in import_request.items]


class ApiTypesFactory:
    @staticmethod
    def history_unit(item: db.SystemItem) -> api.SystemItemHistoryUnit:
        return api.SystemItemHistoryUnit(
            id=item.id,
            type=item.type,
            url=item.url,
            parentId=item.parent_id,
            size=item.size,
            date=item.date
        )

    @classmethod
    def history_response(
            cls, items: list[db.SystemItem]) -> api.SystemItemHistoryResponse:
        return api.SystemItemHistoryResponse(items=[cls.history_unit(item) for item in items])

    @classmethod
    def system_item(cls, root_item: db.SystemItem,
                    child_items: list[db.SystemItem]) -> api.SystemItem:
        # Aux type conversion function
        def _to_item_without_children(system_item: db.SystemItem) -> api.SystemItem:
            h_unit = cls.history_unit(system_item)
            return api.SystemItem(**h_unit.dict(), children=list())

        # Cast db.ItemWithUpdate pairs to api SystemItem instances
        root_item = _to_item_without_children(root_item)
        items = dict()
        for child_item in child_items:
            if not (item := items.get(child_item.parent_id)):
                items[child_item.parent_id] = item = list()
            item.append(_to_item_without_children(child_item))

        # Use BFS to construct the item tree
        not_placed_items = [root_item]
        while not_placed_items:
            current_item = not_placed_items.pop()
            children = items.get(current_item.id, list())
            not_placed_items.extend(children)
            current_item.children.extend(children)

        return root_item
