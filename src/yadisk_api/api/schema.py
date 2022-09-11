from __future__ import annotations
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, validator


class SystemItemType(str, Enum):
    FILE = "FILE"
    FOLDER = "FOLDER"


class SystemItemImport(BaseModel):
    id: str
    type: SystemItemType
    url: str | None
    parentId: str | None
    size: int | None

    @validator("url")
    def validate_url(cls, url: str | None, values):
        _type = values["type"]
        if _type == SystemItemType.FOLDER and url:
            raise ValueError("Item of type 'FOLDER' can't have url")
        if _type == SystemItemType.FILE and not url:
            raise ValueError("Item of type 'FILE' should have url")
        return url

    @validator("size")
    def validate_size(cls, size: int | None, values):
        _type = values["type"]
        if _type == SystemItemType.FOLDER and size:
            raise ValueError("Item of type 'FOLDER' can't have size")
        if _type == SystemItemType.FILE and not size:
            raise ValueError("Item of type 'FILE' should have size")
        return size

    class Config:
        validate_assignment = True
        # orm_mode =True


class SystemItemImportRequest(BaseModel):
    items: list[SystemItemImport]
    updateDate: datetime

    @validator("items")
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
        return [item.parentId for item in self.items]

    class Config:
        validate_assignment = True


class SystemItemHistoryUnit(SystemItemImport):
    date: datetime


class SystemItemHistoryResponse(BaseModel):
    items: list[SystemItemHistoryUnit]


class SystemItem(SystemItemHistoryUnit):
    children: list[SystemItem] | None


class Error(BaseModel):
    code: int
    message: str
