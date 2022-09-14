from datetime import datetime

from src.yadisk_api.db.model import SystemItemType

valid_file_1 = {
    "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
    "type": SystemItemType.FILE,
    "url": "/some/url",
    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
    "size": 42,
    "date": datetime.now(),
    "children": None
}

valid_file_2 = {
    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
    "type": SystemItemType.FILE,
    "url": "/some/url",
    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
    "size": 84,
    "date": datetime.now(),
    "children": None
}

valid_file_3 = {
    "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
    "type": SystemItemType.FILE,
    "url": "/some/url",
    "parentId": None,
    "size": 128,
    "date": datetime.now(),
    "children": None
}

valid_folder_1 = {
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "type": SystemItemType.FOLDER,
    "url": None,
    "parentId": None,
    "size": None,
    "date": datetime.now(),
    "children": []
}

valid_folder_2 = {
    "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
    "type": SystemItemType.FOLDER,
    "url": None,
    "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "size": None,
    "date": datetime.now(),
    "children": []
}
