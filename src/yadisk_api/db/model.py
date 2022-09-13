from enum import Enum as EnumType
from collections import namedtuple
from sqlalchemy import Column, ForeignKeyConstraint, MetaData, Index
from sqlalchemy import String, Integer, Enum, DateTime
from sqlalchemy.orm import declarative_base


class SystemItemType(str, EnumType):
    FILE = "FILE"
    FOLDER = "FOLDER"


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


class SystemItemLink(Base):
    __tablename__ = "system_item_links"

    parent_id = Column(String, primary_key=True)
    child_id = Column(String, primary_key=True)
    date = Column(DateTime(timezone=False), primary_key=True)
    depth = Column(Integer, nullable=False, server_default="1")

    __table_args__ = (
        ForeignKeyConstraint(
            ('parent_id', 'date'),
            ('system_items.id', 'system_items.date'),
            ondelete="CASCADE"
        ),
        ForeignKeyConstraint(
            ('child_id', 'date'),
            ('system_items.id', 'system_items.date'),
            ondelete="CASCADE"
        )
    )


class SystemItem(Base):
    __tablename__ = "system_items"

    id = Column(String, primary_key=True)
    date = Column(DateTime(timezone=False), primary_key=True)
    type = Column(Enum(SystemItemType), nullable=False)
    url = Column(String, nullable=True)
    size = Column(Integer, nullable=True)


ItemWithUpdate = namedtuple("ItemWithUpdate", "item update")
