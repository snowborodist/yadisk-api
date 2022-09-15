import pytest
import copy
from datetime import datetime

from src.yadisk_api.db.model import SystemItemType

valid_file_1 = {
    "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
    "type": SystemItemType.FILE,
    "url": "/some/url",
    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
    "size": 42
}

valid_file_2 = {
    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
    "type": SystemItemType.FILE,
    "url": "/some/url",
    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
    "size": 84
}

valid_file_3 = {
    "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
    "type": SystemItemType.FILE,
    "url": "/some/url",
    "parentId": None,
    "size": 128
}

valid_folder_1 = {
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "type": SystemItemType.FOLDER,
    "url": None,
    "parentId": None,
    "size": None
}

valid_folder_2 = {
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
    "type": SystemItemType.FOLDER,
    "url": None,
    "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "size": None
}

valid_import_request_1 = {
    "items": [
        valid_folder_2,
        valid_file_1,
        valid_file_2
    ],
    "updateDate": "2022-02-11T17:00:00Z"
}


@pytest.fixture
def folder_item_base_schema():
    return copy.deepcopy(valid_folder_1)


@pytest.fixture
def file_item_base_schema():
    return copy.deepcopy(valid_file_1)


@pytest.fixture
def file_item_schema():
    return copy.deepcopy(valid_file_1 | {"date": "2022-02-11T17:00:00Z"})


@pytest.fixture
def folder_item_schema():
    return copy.deepcopy(valid_folder_1 | {"date": "2022-02-11T17:00:00Z"})


@pytest.fixture
def history_unit_schema():
    return copy.deepcopy(valid_file_1 | {"date": "2022-02-11T17:00:00Z"})


@pytest.fixture
def import_request():
    return copy.deepcopy(valid_import_request_1)
