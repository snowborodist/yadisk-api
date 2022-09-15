from src.yadisk_api.services.base import BaseService
from src.yadisk_api.api.schema import SystemItemImportRequest
from src.yadisk_api.db.repository import Repository
from src.yadisk_api.utils.type_conversion import DbTypesFactory


class ImportsService(BaseService):
    async def emplace_imports(self, imports: SystemItemImportRequest):
        async with self.session.begin():
            repo = Repository(self.session)
            if parent_ids := imports.parent_ids:
                await repo.validate_parent_ids(parent_ids)
            items = DbTypesFactory.system_items(imports)
            await repo.insert_items(items)
