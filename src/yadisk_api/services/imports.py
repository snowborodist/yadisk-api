from fastapi import Depends
from databases.core import Connection

from ..utils.db import get_db


class ImportsService:
    def __init__(self, connection: Connection = Depends(get_db)):
        self._conn = connection

    async def foo(self):
        async with self._conn as conn:
            result = await conn.execute("SELECT 1;")
            print(result)