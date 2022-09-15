import pytest
import os
from pathlib import Path
from alembic.config import Config
from alembic.command import upgrade
from sqlalchemy import create_engine, text
from sqlalchemy_utils import create_database, drop_database, database_exists
from fastapi.testclient import TestClient

from src.yadisk_api.app import app
from src.yadisk_api.settings import Settings


def get_test_alembic_config(pg_url: str) -> Config:
    base_path = Path(__file__).parent.parent.resolve()
    config_path = os.path.join(base_path, "alembic.ini")
    config = Config(
        file_=config_path,
        ini_section="alembic")
    alembic_location = config.get_main_option("script_location")
    if not os.path.isabs(alembic_location):
        config.set_main_option(
            "script_location",
            os.path.join(base_path, alembic_location))
    config.set_main_option("sqlalchemy.url", pg_url)
    config.set_main_option("testing", "Yes")
    return config


@pytest.fixture(scope="session")
def get_test_settings():
    settings = Settings()
    settings.database_url = settings.database_url.replace("+asyncpg", "")
    return settings


@pytest.fixture(scope="session", autouse=True)
def database(get_test_settings):
    if database_exists(get_test_settings.database_url):
        drop_database(get_test_settings.database_url)
    create_database(get_test_settings.database_url)
    config = get_test_alembic_config(get_test_settings.database_url)
    upgrade(config, "head")
    try:
        yield
    finally:
        drop_database(get_test_settings.database_url)


@pytest.fixture
def pre_fill_database(get_test_settings):
    engine = create_engine(get_test_settings.database_url)
    with open("initial_data.sql", "r") as script_file:
        escaped_sql = text(script_file.read())
        engine.execute(escaped_sql)
    try:
        yield
    finally:
        engine.execute("""
-- noinspection SqlWithoutWhereForFile
DELETE FROM system_item_links;
DELETE FROM system_items;
DELETE FROM system_item_type_registry;
        """)


@pytest.fixture
def get_test_client():
    yield TestClient(app=app, base_url="http://test")
