from datetime import datetime

from src.yadisk_api.db.model import SystemItemType


class SystemItemParts:
    root_folder = {
        "url": None,
        "size": None,
        "type": "FOLDER",
        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
        "parentId": None,
        "date": "2022-02-02T12:00:00Z"
    }

    sub_folder = {
        "url": None,
        "size": None,
        "type": "FOLDER",
        "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
        "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
        "date": "2022-02-02T12:00:00Z"
    }

    file_one = {
        "type": "FILE",
        "url": "/file/url1",
        "id": "863e1a7a-1304-42ae-943b-179184c077e3",
        "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
        "size": 128,
        "date": "2022-02-02T12:00:00Z"
    }

    file_two = {
        "type": "FILE",
        "url": "/file/url2",
        "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
        "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
        "size": 256,
        "date": "2022-02-02T12:00:00Z"
    }


system_item = SystemItemParts.root_folder | {
    "children": [
        SystemItemParts.sub_folder | {
            "children": [
                SystemItemParts.file_one,
                SystemItemParts.file_two
            ]
        }
    ]
}


#
# {
#     "items": [
#         {
#             "type": "FOLDER",
#             "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
#             "parentId": None
#         }
#     ],
#     "updateDate": "2022-02-01T12:00:00Z"
# },
# {
#     "items": [
#         {
#             "type": "FOLDER",
#             "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
#             "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
#         },
#         {
#             "type": "FILE",
#             "url": "/file/url1",
#             "id": "863e1a7a-1304-42ae-943b-179184c077e3",
#             "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
#             "size": 128
#         },
#         {
#             "type": "FILE",
#             "url": "/file/url2",
#             "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
#             "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
#             "size": 256
#         }
#     ],
#     "updateDate": "2022-02-02T12:00:00Z"
# },
#
#
# class SampleData:
#     class SystemItemBases:
#         root_folder = {
#             "url": None,
#             "size": None,
#             "type": "FOLDER",
#             "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
#             "parentId": None
#         }
#
#         sub_folder = {
#             "url": None,
#             "size": None,
#             "type": "FOLDER",
#             "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
#             "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
#         }
#
#         file_one = {
#             "type": "FILE",
#             "url": "/file/url1",
#             "id": "863e1a7a-1304-42ae-943b-179184c077e3",
#             "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
#             "size": 128
#         }
#
#         file_two = {
#             "type": "FILE",
#             "url": "/file/url2",
#             "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
#             "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
#             "size": 256
#         }
#
#     class SystemItemParts:
#         root_folder = {
#             "url": None,
#             "size": None,
#             "type": "FOLDER",
#             "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
#             "parentId": None,
#             "date": "2022-02-02T12:00:00Z"
#         }
#
#         sub_folder = {
#             "url": None,
#             "size": None,
#             "type": "FOLDER",
#             "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
#             "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
#             "date": "2022-02-02T12:00:00Z"
#         }
#
#         file_one = {
#             "type": "FILE",
#             "url": "/file/url1",
#             "id": "863e1a7a-1304-42ae-943b-179184c077e3",
#             "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
#             "size": 128,
#             "date": "2022-02-02T12:00:00Z"
#         }
#
#         file_two = {
#             "type": "FILE",
#             "url": "/file/url2",
#             "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
#             "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
#             "size": 256,
#             "date": "2022-02-02T12:00:00Z"
#         }
#
#     system_item = SystemItemParts.root_folder | {
#         "children": [
#             SystemItemParts.sub_folder | {
#                 "children": [
#                     SystemItemParts.file_one,
#                     SystemItemParts.file_two
#                 ]
#             }
#         ]
#     }
#
#     system_item_import_request = {
#         "items": [SystemItemBases.root_folder,
#                   SystemItemBases.sub_folder,
#                   SystemItemBases.file_one,
#                   SystemItemBases.file_two],
#         "updateDate": datetime.fromisoformat("2022-05-28T21:12:01.000Z")
#     }
#
#     system_item_history_unit = \
#         system_item_base | \
#         {"date": datetime.fromisoformat("2022-05-28T21:12:01.000Z")}
#
#     system_item_history_response = {
#         "items": [system_item_history_unit]
#     }
#
#     system_item = system_item_base | {"children": []}
