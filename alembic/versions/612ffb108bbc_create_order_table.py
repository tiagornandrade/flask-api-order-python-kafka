"""create order table

Revision ID: 612ffb108bbc
Revises: 
Create Date: 2023-07-13 12:29:26.541459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '612ffb108bbc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()





def upgrade_engine1() -> None:
    op.create_table(
        'order',
        sa.Column('user_id', sa.Text),
        sa.Column('order_id', sa.Text),
        sa.Column('event_key', sa.Text),
        sa.Column('product_name', sa.Text),
        sa.Column('description', sa.Text),
        sa.Column('price', sa.Float),
        sa.Column('event_timestamp', sa.TIMESTAMP),
        sa.Column('operation', sa.Text)
    )


def downgrade_engine1() -> None:
    op.drop_table('order')


def upgrade_engine2() -> None:
    op.create_table(
        'order',
        sa.Column('user_id', sa.Text),
        sa.Column('order_id', sa.Text),
        sa.Column('event_key', sa.Text),
        sa.Column('product_name', sa.Text),
        sa.Column('description', sa.Text),
        sa.Column('price', sa.Float),
        sa.Column('event_timestamp', sa.TIMESTAMP),
        sa.Column('operation', sa.Text)
    )


def downgrade_engine2() -> None:
    op.drop_table('order')

