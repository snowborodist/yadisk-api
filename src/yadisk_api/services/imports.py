from .base import BaseService
from ..api.schema import SystemItemImportRequest
from ..db.repositories.SystemItemRepository import SystemItemRepository
from ..utils.type_conversion import DbTypesFactory


class ImportsService(BaseService):
    async def emplace_imports(self, imports: SystemItemImportRequest):
        async with self.session.begin():
            # Convert schema to db model
            items, updates = DbTypesFactory.system_items(imports)
            # Check if there are no FILE item ids among parent_ids of the items to be emplaced
            repo = SystemItemRepository(self.session)
            await repo.validate_parent_ids(imports.parent_ids)
            # Filter out existing SystemItem records (== ON CONFLICT DO NOTHING)
            emplacing_item_ids = [item.id for item in items]
            existing_item_ids = await repo.get_existing_item_ids(emplacing_item_ids)
            items = list(filter(lambda x: x.id not in existing_item_ids, items))
            # Write all the stuff to DB
            await repo.emplace_items(items)
            await repo.emplace_item_updates(updates)
