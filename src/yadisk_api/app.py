from fastapi import FastAPI

from src.yadisk_api.api import router
from src.yadisk_api.utils.exception_handling import setup_exception_handling

app = FastAPI()
app.include_router(router)
setup_exception_handling(app)
