from sqlalchemy import Column, ForeignKey, MetaData
from sqlalchemy import String, Integer, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base

from ..api.schema import SystemItemType


convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


class SystemItem(Base):
    __tablename__ = "system_items"

    id = Column(String, primary_key=True)
    type = Column(Enum(SystemItemType), nullable=False)


class SystemItemUpdate(Base):
    __tablename__ = "item_updates"

    id = Column(Integer, primary_key=True)
    item_id = Column(String, ForeignKey("system_items.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(String, ForeignKey("system_items.id"), nullable=True)
    date = Column(DateTime(timezone=False), nullable=False)
    url = Column(String, nullable=True)
    size = Column(Integer, nullable=True)
