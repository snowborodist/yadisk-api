from sqlalchemy import Column, ForeignKeyConstraint, MetaData
from sqlalchemy import String, Integer, Enum, DateTime, BigInteger
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
