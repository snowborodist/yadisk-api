import pytest
from uuid import uuid4
from yarl import URL
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, drop_database


from src.yadisk_api.settings import Settings

settings = Settings(_env_file=".test.env", _env_file_encoding="utf-8")


@pytest.fixture
def database():
    tmp_db_name = '.'.join([uuid4().hex, 'test'])
    tmp_db_url = str(URL(settings.database_url).with_path(tmp_db_name))
    create_database(tmp_db_url)
    try:
        yield tmp_db_url
    finally:
        drop_database(tmp_db_url)

# @pytest.fixture
# def migrated_db_engine(db_engine):
#     async with db_engine.connect() as conn:
#         await conn.run_sync(metadata.create_all)
#     return db_engine
#
#
# @pytest.fixture
# def db_session(migrated_db_engine):
#     Session = sessionmaker(migrated_db_engine, class_=AsyncSession)
#     session: AsyncSession = Session()
#     try:
#         yield session
#     finally:
#         session.close()
#
#
# @pytest.fixture
# def api_client(db_session):
#     return TestClient(app)
