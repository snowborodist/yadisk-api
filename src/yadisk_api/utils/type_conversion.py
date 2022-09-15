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
            size=item_import.size if item_import.size else 0
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
    def system_item_from_adj_list(cls, root_item: db.SystemItem,
                                  child_items: list[db.SystemItem]) -> api.SystemItem:
        """
        Возвращает объект схемы api.SystemItem, построенный из элементов списка смежности dbSystemItem,
        с восстановленным деревом потомков, актуализированными размерами и датами обновления элементов.
        @param root_item: корневой элемент списка смежности.
        @param child_items: дочерние элементы списка смежности.
        @return: построенный объект схемы api.SystemItem.
        """
        # Вспомогательная функция
        def _to_item_without_children(system_item: db.SystemItem) -> api.SystemItem:
            h_unit = cls.history_unit(system_item)
            return api.SystemItem(**h_unit.dict())

        # Предварительная конвертация типов db.SystemItem -> api.SystemItem
        root_item = _to_item_without_children(root_item)
        items = dict()
        deletion_dates = []
        for child_item in child_items:
            if child_item.deleted:
                deletion_dates.append(child_item.date)
                continue
            if not (item := items.get(child_item.parent_id)):
                items[child_item.parent_id] = item = list()
            item.append(_to_item_without_children(child_item))
        if deletion_dates:
            deletion_dates.append(root_item.date)
            root_item.date = max(deletion_dates)

        # Построение дерева потомков методом BFS.
        not_placed_items = [root_item]
        while not_placed_items:
            current_item = not_placed_items.pop()
            if current_item.type == db.SystemItemType.FILE:
                continue
            children = items.get(current_item.id, list())
            not_placed_items.extend(children)
            current_item.children = children

        # Рекурсивное заполнение дерева потомков актуальными размерами и датами изменений.
        _, _ = cls._fill_system_item_tree(root_item)
        return root_item

    @classmethod
    def _fill_system_item_tree(cls, root_item: api.SystemItem) -> (int, datetime):
        dts = [root_item.date, ]
        size = root_item.size
        if root_item.children:
            for child in root_item.children:
                s, dt = cls._fill_system_item_tree(child)
                dts.append(dt)
                size += s
            root_item.size = size
            root_item.date = max(dts)
        return root_item.size, root_item.date
