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
            cls, items_updates: list[(db.SystemItem, db.SystemItemUpdate)]) -> api.SystemItemHistoryResponse:
        return api.SystemItemHistoryResponse(
            items=[cls.history_unit(item, update)
                   for item, update in items_updates]
        )
