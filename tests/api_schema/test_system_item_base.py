import pytest
from pydantic.error_wrappers import ValidationError

from src.yadisk_api.api.schema import SystemItemBase


# incoming data validation tests:
def test_item_id_is_required(file_item_base_schema):
    file_item_base_schema["id"] = None
    with pytest.raises(ValidationError):
        SystemItemBase.parse_obj(file_item_base_schema)
    file_item_base_schema.pop("id")
    with pytest.raises(ValidationError):
        SystemItemBase.parse_obj(file_item_base_schema)


def test_parent_id_is_not_required(file_item_base_schema):
    SystemItemBase.parse_obj(file_item_base_schema)
    file_item_base_schema["parentId"] = None
    SystemItemBase.parse_obj(file_item_base_schema)
    file_item_base_schema.pop("parentId")
    SystemItemBase.parse_obj(file_item_base_schema)


def test_type_is_required(file_item_base_schema):
    file_item_base_schema["type"] = None
    with pytest.raises(ValidationError):
        SystemItemBase.parse_obj(file_item_base_schema)
    file_item_base_schema.pop("type")
    with pytest.raises(ValidationError):
        SystemItemBase.parse_obj(file_item_base_schema)


def test_type_accepts_only_allowed_values(file_item_base_schema):
    file_item_base_schema["type"] = "NOT VALID"
    with pytest.raises(ValidationError):
        SystemItemBase.parse_obj(file_item_base_schema)


def test_size_must_be_ge_0(file_item_base_schema):
    file_item_base_schema["size"] = -100
    with pytest.raises(ValidationError):
        SystemItemBase.parse_obj(file_item_base_schema)


def test_url_length_is_from_0_to_255_inclusively(file_item_base_schema):
    file_item_base_schema["url"] = ""
    SystemItemBase.parse_obj(file_item_base_schema)
    file_item_base_schema["url"] = "a" * 128
    SystemItemBase.parse_obj(file_item_base_schema)
    file_item_base_schema["url"] = "a" * 255
    SystemItemBase.parse_obj(file_item_base_schema)
    file_item_base_schema["url"] = "a" * 1024
    with pytest.raises(ValidationError):
        SystemItemBase.parse_obj(file_item_base_schema)
