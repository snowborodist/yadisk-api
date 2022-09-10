from fastapi import Depends
from databases.core import Connection

from ..utils.db import get_db


class BaseService:
    def __init__(self, connection: Connection = Depends(get_db)):
        self._conn = connection
