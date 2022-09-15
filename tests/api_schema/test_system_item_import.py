import pytest
from pydantic.error_wrappers import ValidationError

from src.yadisk_api.api.schema import SystemItemImport


# incoming data validation tests:
def test_url_is_required_if_file_type(file_item_base_schema):
    file_item_base_schema["url"] = None
    with pytest.raises(ValidationError):
        SystemItemImport.parse_obj(file_item_base_schema)


def test_size_is_required_if_file_type(file_item_base_schema):
    file_item_base_schema["size"] = None
    with pytest.raises(ValidationError):
        SystemItemImport.parse_obj(file_item_base_schema)


def test_size_must_be_null_for_folders(folder_item_base_schema):
    folder_item_base_schema["size"] = 100
    with pytest.raises(ValidationError):
        SystemItemImport.parse_obj(folder_item_base_schema)


def test_url_must_be_null_for_folders(folder_item_base_schema):
    folder_item_base_schema["url"] = "/not/null/url"
    with pytest.raises(ValidationError):
        SystemItemImport.parse_obj(folder_item_base_schema)
