from src.yadisk_api.api.schema import SystemItem

from .conftest import valid_folder_1


def test_accepts_folder_data_with_size():
    item_json = valid_folder_1.copy()
    item_json["size"] = 1024
    item = SystemItem.parse_obj(item_json)
    assert item.size == 1024
