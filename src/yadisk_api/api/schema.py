from __future__ import annotations
from enum import Enum
from datetime import datetime

from pydantic import BaseModel


class SystemItemType(str, Enum):
    FILE = "FILE"
    FOLDER = "FOLDER"


class SystemItemImport(BaseModel):
    id: str
    url: str | None
    parentId: str | None
    type: SystemItemType
    size: int | None

    class Config:
        orm_mode = True


class SystemItemImportRequest(BaseModel):
    items: list[SystemItemImport]
    updateDate: datetime


class SystemItemHistoryUnit(SystemItemImport):
    date: datetime


class SystemItemHistoryResponse(BaseModel):
    items: list[SystemItemHistoryUnit]


class SystemItem(SystemItemHistoryUnit):
    children: list[SystemItem] | None


class Error(BaseModel):
    code: int
    message: str
