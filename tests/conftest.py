# import pytest
# from uuid import uuid4
# from yarl import URL
# from fastapi.testclient import TestClient
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
#
# from src.yadisk_api.app import app
# from src.yadisk_api.settings import settings
# from src.yadisk_api.db.model import metadata
#
#
# @pytest.fixture
# def db_engine():
#     tmp_db_name = '.'.join([uuid4().hex, 'test'])
#     tmp_db_url = str(URL(settings.database_url).with_path(tmp_db_name))
#     engine = create_async_engine(tmp_db_url)
#
#     try:
#         yield engine
#     finally:
#         engine.dispose()
#
#
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
