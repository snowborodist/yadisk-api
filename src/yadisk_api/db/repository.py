from asyncio import gather
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert

from src.yadisk_api.db import model as db
from src.yadisk_api.utils.exception_handling import ItemNotFoundError, InvalidDataError


class Repository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def validate_item_exists(self, system_item_id: str, due_date: datetime | None = None):
        """
        Проверяет существует ли объект system_item с заданным id.
        Если объект не существует или был удален, то кидает исключение ItemNotFoundError.
        @param system_item_id: id бъекта для проверки.
        @param due_date: дата, по состоянию на которую (включительно) проводится проверка.
        """
        filters = [db.SystemItem.id == system_item_id, ]
        if due_date:
            filters.append(db.SystemItem.date <= due_date)
        # noinspection PyUnresolvedReferences
        stmt = select(db.SystemItem.deleted) \
            .distinct(db.SystemItem.id).where(*filters) \
            .order_by(db.SystemItem.id, db.SystemItem.date.desc())
        rows = list(await self.session.execute(stmt))
        if not rows:
            raise ItemNotFoundError
        deleted, *_ = rows[0]
        if deleted:
            raise ItemNotFoundError

    async def validate_parent_ids(self, parent_ids: list[str]):
        """
        Проверяет, что объекты в базе данных с переданными id имеют тип 'FOLDER'.
        Иначе кидает исключение InvalidDataError.
        @param parent_ids: список id для проверки.
        """
        # noinspection PyUnresolvedReferences
        rows = await self.session.execute(
            select(db.SystemItem).filter(db.SystemItem.type == db.SystemItemType.FILE,
                                         db.SystemItem.id.in_(parent_ids))
        )
        for _ in rows:
            raise InvalidDataError("Imported items contain parent links to items of type 'FILE'")

    async def insert_items(self, items: list[db.SystemItem]):
        """
        Производит вставку новых и обновление существущих объектов в базе данных.
        @param items: список объектов для вставки.
        """
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
        # TODO: gather?
        # for item in items:
        #     if parent_id := item.parent_id:
        #         await self._link_children(parent_id, item.id, item.date)
        await gather(*[self._link_children(item.parent_id, item.id, item.date)
                      for item in items if item.parent_id])

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
            self, system_item_id: str,
            due_date: datetime | None = None) -> list[db.SystemItem]:
        """
        Возвращает объекты system_item, которые образуют список смежности
        от определенного корневого объекта.
        Корневой элемент всегда является первым элементов возвращаемого списка.
        @param system_item_id: идентификатор корневого элемента возвращаемого списка.
        @param due_date: верхняя граница даты, для которой (включительно) нужно построить список смежности.
        Если не указана, то строится актуальный на момент запроса список.
        @return список смежности для заданного system_item. Первый элемент списка - корневой.
        """
        stmt = select(db.SystemItem) \
            .join(db.SystemItemLink,
                  db.SystemItem.id == db.SystemItemLink.child_id) \
            .distinct(db.SystemItem.id)
        if due_date:
            # noinspection PyUnresolvedReferences
            stmt = stmt.where(and_(db.SystemItemLink.parent_id == system_item_id,
                                   db.SystemItem.date <= due_date))
        else:
            stmt = stmt.where(db.SystemItemLink.parent_id == system_item_id)
        # noinspection PyUnresolvedReferences
        stmt = stmt.order_by(db.SystemItem.id, db.SystemItem.date.desc(), db.SystemItemLink.depth)

        rows = await self.session.execute(stmt)
        # TODO: Make the root first!!!!
        return [row for row, *_ in rows]

    async def get_file_updates(
            self, date_start: datetime, date_end: datetime) -> list[db.SystemItem]:
        """
        Возвращает изменения файлов в заданном временном интервале [date_start, date_end].
        @param date_start: начальная дата интервала.
        @param date_end: конечная дата интервала.
        @return: список изменений файлов.
        """
        # noinspection PyUnresolvedReferences
        stmt = select(db.SystemItem) \
            .filter(db.SystemItem.type == db.SystemItemType.FILE,
                    db.SystemItem.date.between(date_start, date_end))
        rows = await self.session.execute(stmt)
        return [row for row, *_ in rows]

    async def get_history_points_for_item(
            self, system_item_id: str,
            date_start: datetime | None = None,
            date_end: datetime | None = None) -> list[datetime]:
        """
        Возвращает список дат изменений для элемента system_item с заданным идентификатором.
        Список может быть ограничен параметрами: [date_start, date_end).
        @param system_item_id: идентификатор элемента system_item,
        для которого нужно вернуть список дат изменений.
        @param date_start: нижняя временная граница для возвращаемого списка.
        При отсутствии значения - список строится без учета нижней временной границы.
        @param date_end: верхняя временная граница для возвращаемого списка.
        При отсутствии значения - список строится без учета верхней временной границы.
        @return: список дат изменений заданного элемента system_item.
        """
        where_clauses = [db.SystemItemLink.parent_id == system_item_id, ]
        if date_start:
            where_clauses.append(db.SystemItemLink.date >= date_start)
        if date_end:
            where_clauses.append(db.SystemItemLink.date < date_end)
        stmt = select(db.SystemItemLink.date).distinct().where(and_(*where_clauses))
        return list(await self.session.execute(stmt))
