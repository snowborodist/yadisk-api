import pytest
from pydantic.error_wrappers import ValidationError

from src.yadisk_api.api.schema import SystemItemImportRequest


# incoming data validation tests:
def test_item_ids_are_cross_unique(import_request, file_item_base_schema):
    import_request["items"].extend([file_item_base_schema, file_item_base_schema])
    with pytest.raises(ValidationError):
        SystemItemImportRequest.parse_obj(import_request)


def test_only_folders_can_be_parents(import_request, file_item_base_schema, folder_item_base_schema):
    folder_item_base_schema["parentId"] = file_item_base_schema["id"]
    import_request["items"].extend([file_item_base_schema, folder_item_base_schema])
    with pytest.raises(ValidationError):
        SystemItemImportRequest.parse_obj(import_request)


def test_update_date_accepts_only_iso_8601(import_request):
    SystemItemImportRequest.parse_obj(import_request)
    import_request["updateDate"] = "2022-02-11T17:00:00"
    SystemItemImportRequest.parse_obj(import_request)
    import_request["updateDate"] = "2022-02-11 17-00-00"
    with pytest.raises(ValidationError):
        SystemItemImportRequest.parse_obj(import_request)
