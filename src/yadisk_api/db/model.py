from enum import Enum as EnumType
from sqlalchemy import Column, MetaData, ForeignKey
from sqlalchemy import String, Integer, Enum, DateTime, Boolean
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
    date = Column(DateTime, primary_key=True)
    depth = Column(Integer, nullable=False)


class SystemItem(Base):
    __tablename__ = "system_items"

    id = Column(String, primary_key=True)
    parent_id = Column(String, ForeignKey("system_item_type_registry.system_item_id"), nullable=True)
    date = Column(DateTime, primary_key=True)
    type = Column(Enum(SystemItemType), nullable=False)
    url = Column(String, nullable=True)
    size = Column(Integer, nullable=False)
    deleted = Column(Boolean, nullable=False, default=False)


class SystemItemTypeMatch(Base):
    __tablename__ = "system_item_type_registry"

    system_item_id = Column(String, primary_key=True)
    system_item_type = Column(Enum(SystemItemType), nullable=False)

# TODO: Add indexes (parent, date, child), (child, parent, date)
