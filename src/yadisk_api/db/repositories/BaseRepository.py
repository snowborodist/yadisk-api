from databases.core import Connection


class BaseRepository:
    def __init__(self, connection: Connection):
        self._conn = connection
