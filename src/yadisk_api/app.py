from fastapi import FastAPI

from .utils.db import init_db
from .api import router

app = FastAPI()
app.include_router(router)
init_db(app)



# TODO: Organize requirements!
# Package           Version
# httptools         0.4.0
# idna              3.3
# pip               21.1.2
# pydantic          1.9.0
# python-dotenv     0.21.0
# PyYAML            6.0
# setuptools        57.0.0
# sniffio           1.3.0
# starlette         0.17.1
# typing-extensions 4.3.0
# uvicorn           0.18.3
# watchfiles        0.16.1
# websockets        10.3
# wheel             0.36.2
