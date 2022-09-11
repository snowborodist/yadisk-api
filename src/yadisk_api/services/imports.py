from .base import BaseService
from ..api.schema import SystemItemImportRequest
from ..db.repositories.SystemItemRepository import SystemItemRepository


class ImportsService(BaseService):
    async def emplace_imports(self, imports: SystemItemImportRequest):
        async with self.session.begin():
            repo = SystemItemRepository(self.session)
            res = await self.session.execute("SELECT 1;")
            print(res.scalars().first())
        # TODO: logic here

