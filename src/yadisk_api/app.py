from fastapi import FastAPI

from .utils.db import init_db
from .api import router

app = FastAPI()
app.include_router(router)
init_db(app)
