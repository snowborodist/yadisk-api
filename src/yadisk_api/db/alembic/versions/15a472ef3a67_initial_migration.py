"""initial migration

Revision ID: 15a472ef3a67
Revises: 
Create Date: 2022-09-11 11:29:56.850418

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '15a472ef3a67'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('system_items',
                    sa.Column('id', sa.String(), nullable=False),
                    sa.Column('type', sa.Enum('FILE', 'FOLDER', name='systemitemtype'), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk__system_items'))
                    )
    # noinspection PyTypeChecker
    op.create_table('item_updates',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('item_id', sa.String(), nullable=False),
                    sa.Column('parent_id', sa.String(), nullable=True),
                    sa.Column('date', sa.DateTime(), nullable=False),
                    sa.Column('url', sa.String(), nullable=True),
                    sa.Column('size', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['item_id'], ['system_items.id'],
                                            name=op.f('fk__item_updates__item_id__system_items'), ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['parent_id'], ['system_items.id'],
                                            name=op.f('fk__item_updates__parent_id__system_items')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk__item_updates'))
                    )
    op.execute("""
        CREATE FUNCTION check_type_change() RETURNS TRIGGER LANGUAGE plpgsql AS $$
        BEGIN
            IF OLD.type <> NEW.type THEN
                RAISE EXCEPTION 'cannot change type'; 
            END IF;
            RETURN NEW;
        END $$;
        
        CREATE TRIGGER type_update_trigger BEFORE UPDATE ON system_items FOR EACH ROW
              EXECUTE PROCEDURE check_type_change();
    """)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('item_updates')
    op.drop_table('system_items')
    # ### end Alembic commands ###