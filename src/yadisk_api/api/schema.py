from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, validator, conint, constr

from ..db.model import SystemItemType


class SystemItemBase(BaseModel):
    id: str
    type: SystemItemType
    url: constr(max_length=255) | None
    parentId: str | None
    size: conint(ge=0) | None


class SystemItemImport(SystemItemBase):
    @validator("url", always=True)
    def validate_url(cls, url: str | None, values):
        _type = values["type"]
        if _type == SystemItemType.FOLDER and url:
            raise ValueError("Item of type 'FOLDER' can't have url")
        if _type == SystemItemType.FILE and not url:
            raise ValueError("Item of type 'FILE' should have url")
        return url

    @validator("size", always=True)
    def validate_size(cls, size: int | None, values):
        _type = values["type"]
        if _type == SystemItemType.FOLDER and size:
            raise ValueError("Item of type 'FOLDER' can't have size")
        if _type == SystemItemType.FILE and not size:
            raise ValueError("Item of type 'FILE' should have size")
        return size

    class Config:
        validate_assignment = True


class SystemItemImportRequest(BaseModel):
    items: list[SystemItemImport]
    updateDate: datetime

    @validator("items", always=True)
    def validate_parents(cls, items: list[SystemItemImport]):
        new_file_ids = set()
        new_parent_rel_ids = set()
        for item in items:
            if item.type == SystemItemType.FILE:
                new_file_ids.add(item.id)
            if item.parentId:
                new_parent_rel_ids.add(item.parentId)
        if new_file_ids & new_parent_rel_ids:
            raise ValueError("Items of type 'FILE' can't be parents")
        return items

    @property
    def parent_ids(self) -> list[str]:
        return [item.parentId for item in self.items if item.parentId is not None]

    class Config:
        validate_assignment = True


class SystemItemHistoryUnit(SystemItemBase):
    date: datetime


class SystemItemHistoryResponse(BaseModel):
    items: list[SystemItemHistoryUnit]

    class Config:
        orm_mode = True


class SystemItem(SystemItemHistoryUnit):
    children: list[SystemItem]

    class Config:
        orm_mode = True

    @property
    def history_unit(self) -> SystemItemHistoryUnit:
        return SystemItemHistoryUnit.parse_obj(self)


class Error(BaseModel):
    code: int
    message: str
