from .base import BaseService
from ..api.schema import SystemItemImportRequest
from ..db.repository import Repository
from ..utils.type_conversion import DbTypesFactory


class ImportsService(BaseService):
    async def emplace_imports(self, imports: SystemItemImportRequest):
        async with self.session.begin():
            repo = Repository(self.session)
            await repo.validate_parent_ids(imports.parent_ids)
            items, updates = DbTypesFactory.system_items(imports)
            await repo.upsert_items(items)
            await repo.insert_item_updates(updates)
