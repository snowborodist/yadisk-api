from .base import BaseService
from ..api.schema import SystemItemImportRequest
from ..db.repositories.SystemItemRepository import SystemItemRepository


class ImportsService(BaseService):
    async def emplace_imports(self, imports: SystemItemImportRequest):
        async with self.session.begin():
            repo = SystemItemRepository(self.session)
            await repo.validate_parent_ids(imports.parent_ids)
            await repo.insert_imports(imports)
