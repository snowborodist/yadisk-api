from sqlalchemy.orm.session import make_transient

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
            existing_parents = [p for p in await repo.get_existing_parents(imports.item_ids)
                                if p.id not in imports.item_ids]
            for e_parent in existing_parents:
                self.session.expunge(e_parent)
                make_transient(e_parent)
                e_parent.date = imports.updateDate.replace(tzinfo=None)
            items = DbTypesFactory.system_items(imports)
            items.extend(existing_parents)
            await repo.insert_items(items)
