import datetime

from src.yadisk_api.db.model import SystemItemType
from src.yadisk_api.api.schema import SystemItemImport
from src.yadisk_api.utils.type_conversion import ApiTypesFactory, DbTypesFactory

file_1 = {
    "id": "f1",
    "type": SystemItemType.FILE,
    "url": "/some/url",
    "parentId": "fld1",
    "size": 42
}

file_2 = {
    "id": "f2",
    "type": SystemItemType.FILE,
    "url": "/some/url",
    "parentId": "fld1",
    "size": 84
}

file_3 = {
    "id": "f3",
    "type": SystemItemType.FILE,
    "url": "/some/url",
    "parentId": "fld2",
    "size": 168
}

folder_1 = {
    "id": "fld1",
    "type": SystemItemType.FOLDER,
    "url": None,
    "parentId": "fld2",
    "size": None
}

folder_2 = {
    "id": "fld2",
    "type": SystemItemType.FOLDER,
    "url": None,
    "parentId": None,
    "size": None
}

folder_3 = {
    "id": "fld3",
    "type": SystemItemType.FOLDER,
    "url": None,
    "parentId": "fld1",
    "size": None
}

#
#               fld2
#              /   \
#            /      \
#          fld1     f3
#        /  |  \
#      /    |   \
#     f1   f2   fld3
#

date_1 = datetime.datetime.strptime("2022-02-01T17:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
date_2 = datetime.datetime.strptime("2022-02-02T17:00:00Z", "%Y-%m-%dT%H:%M:%SZ")
date_3 = datetime.datetime.strptime("2022-02-03T17:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

fld1 = DbTypesFactory.system_item(SystemItemImport.parse_obj(folder_1), date_3)
fld2 = DbTypesFactory.system_item(SystemItemImport.parse_obj(folder_2), date_1)
fld3 = DbTypesFactory.system_item(SystemItemImport.parse_obj(folder_3), date_1)
f1 = DbTypesFactory.system_item(SystemItemImport.parse_obj(file_1), date_1)
f2 = DbTypesFactory.system_item(SystemItemImport.parse_obj(file_2), date_3)
f3 = DbTypesFactory.system_item(SystemItemImport.parse_obj(file_2), date_2)

root = fld2
others = [fld1, fld3, f1, f2, f3]


def test_api_system_item_is_built_properly():
    constructed = ApiTypesFactory.system_item_from_adj_list(root, others)

    assert constructed.size == f1.size + f2.size + f3.size
    assert constructed.date == date_3
