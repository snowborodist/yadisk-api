from fastapi import FastAPI
from databases import Database
from databases.core import Connection

from src.yadisk_api.settings import settings

database = Database(settings.database_url)


def init_db(app: FastAPI):
    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()


async def get_db() -> Connection:
    return database.connection()
