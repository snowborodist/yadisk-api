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
            date=date,
            url=item_import.url,
            size=item_import.size
        )
        return item, update

    @classmethod
    def system_items(cls, import_request: api.SystemItemImportRequest) \
            -> list[(db.SystemItem, db.SystemItemUpdate)]:
        return [
            cls.system_item(
                item_import,
                import_request.updateDate)
            for item_import in import_request.items
        ]


class ApiTypesFactory:
    pass
