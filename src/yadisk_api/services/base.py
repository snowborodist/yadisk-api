from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..utils.db import get_session


class BaseService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session
