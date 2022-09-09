from sqlalchemy import Column, ForeignKeyConstraint
from sqlalchemy import String, Integer, Enum, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base

from ..api.schema import SystemItemType

Base = declarative_base()


class SystemItem(Base):
    __tablename__ = "system_items"

    id = Column(String, primary_key=True)
    date = Column(DateTime(timezone=False), primary_key=True)
    url = Column(String, nullable=True)
    parent_id = Column(String, nullable=True)
    type = Column(Enum(SystemItemType), nullable=False)
    size = Column(Integer, nullable=True)


class ItemTreePath(Base):
    __tablename__ = "item_tree_paths"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ancestor_id = Column(String, nullable=False)
    ancestor_date = Column(DateTime(timezone=False), nullable=False)
    descendant_id = Column(String, nullable=False)
    descendant_date = Column(DateTime(timezone=False), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            (ancestor_id, ancestor_date),
            [SystemItem.id, SystemItem.date]
        ),
        ForeignKeyConstraint(
            (descendant_id, descendant_date),
            [SystemItem.id, SystemItem.date]
        )
    )
