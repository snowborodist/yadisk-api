from fastapi import FastAPI
from databases import Database

from src.yadisk_api.settings import settings

database = Database(settings.database_url)


def init_db(app: FastAPI):
    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()


# TODO: Get return type from database docs
async def get_db() -> any:
    return database.connection()
