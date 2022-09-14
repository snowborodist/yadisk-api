from fastapi import FastAPI

from .api import router
from .utils.exception_handling import setup_exception_handling

app = FastAPI()
app.include_router(router)
setup_exception_handling(app)
