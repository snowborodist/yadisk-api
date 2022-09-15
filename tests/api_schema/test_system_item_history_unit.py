import pytest
import json
from pydantic.error_wrappers import ValidationError

from src.yadisk_api.api.schema import SystemItemHistoryUnit


# incoming data validation tests:
def test_date_accepts_only_iso_8601(history_unit_schema):
    SystemItemHistoryUnit.parse_obj(history_unit_schema)
    history_unit_schema["date"] = "2022-02-11T17:00:00"
    SystemItemHistoryUnit.parse_obj(history_unit_schema)
    history_unit_schema["date"] = "2022-02-11 17-00-00"
    with pytest.raises(ValidationError):
        SystemItemHistoryUnit.parse_obj(history_unit_schema)


# output data format tests:
def test_formats_date_in_iso_8601(history_unit_schema):
    history_unit_schema["date"] = "2022-02-11T17:00:00Z"
    h_unit = SystemItemHistoryUnit.parse_obj(history_unit_schema)
    h_unit_render = json.loads(h_unit.json())
    assert history_unit_schema["date"] == h_unit_render["date"]


def test_renders_null_url_field(history_unit_schema):
    history_unit_schema.pop("url")
    h_unit = SystemItemHistoryUnit.parse_obj(history_unit_schema).dict()
    assert h_unit["url"] is None


def test_renders_null_parent_id_field(history_unit_schema):
    history_unit_schema.pop("parentId")
    h_unit = SystemItemHistoryUnit.parse_obj(history_unit_schema).dict()
    assert h_unit["parentId"] is None
