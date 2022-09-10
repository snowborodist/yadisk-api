from .base import BaseService
from ..api.schema import SystemItemImportRequest
from ..db.repositories.SystemItemRepository import SystemItemRepository


class ImportsService(BaseService):
    async def emplace_imports(self, imports: SystemItemImportRequest):
        async with self._conn as conn:
            repo = SystemItemRepository(conn)
            pass
        # TODO: logic here

