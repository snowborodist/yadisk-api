from .BaseRepository import BaseRepository
from ...api.schema import SystemItemImportRequest, SystemItem, SystemItemType

from sqlalchemy.dialects.postgresql import insert as pg_insert


class SystemItemRepository(BaseRepository):
    async def get_type_if_exists(self, item_id: str) -> SystemItemType | None:
        pass

    async def emplace_many(self, imports: SystemItemImportRequest):
        pass

    async def get(self) -> SystemItem | None:
        pass

    async def delete(self, system_item_id: str):
        pass
