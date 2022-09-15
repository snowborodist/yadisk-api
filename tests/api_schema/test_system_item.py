from src.yadisk_api.api.schema import SystemItem


def test_accepts_folder_data_with_size(folder_item_schema):
    item_json = folder_item_schema.copy()
    item_json["size"] = 1024
    item = SystemItem.parse_obj(item_json)
    assert item.size == 1024
