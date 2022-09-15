from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from src.yadisk_api.api.schema import Error


class ItemNotFoundError(Exception):
    pass


class InvalidDataError(Exception):
    def __init__(self, message: str):
        self.message = message


def setup_exception_handling(app: FastAPI):
    @app.exception_handler(ItemNotFoundError)
    async def item_not_found_handler(*_):
        return JSONResponse(status_code=404, content=Error.not_found_error().dict())

    @app.exception_handler(InvalidDataError)
    async def invalid_data_handler(*_):
        return JSONResponse(status_code=400, content=Error.validation_error().dict())

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(*_):
        return JSONResponse(status_code=400, content=Error.validation_error().dict())

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_error_handler(*_):
        return JSONResponse(status_code=400, content=Error.validation_error().dict())
