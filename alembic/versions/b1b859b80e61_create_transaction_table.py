"""create transaction table

Revision ID: b1b859b80e61
Revises: 612ffb108bbc
Create Date: 2023-07-13 12:29:29.145794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1b859b80e61'
down_revision = '612ffb108bbc'
branch_labels = None
depends_on = None


def upgrade(engine_name: str) -> None:
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name: str) -> None:
    globals()["downgrade_%s" % engine_name]()





def upgrade_engine1() -> None:
    op.create_table(
        'transaction',
        sa.Column('transaction_id', sa.TEXT),
        sa.Column('transaction', sa.JSON)
    )


def downgrade_engine1() -> None:
    op.drop_table('transaction')


def upgrade_engine2() -> None:
    op.create_table(
        'transaction',
        sa.Column('transaction_id', sa.TEXT),
        sa.Column('transaction', sa.JSON)
    )


def downgrade_engine2() -> None:
    op.drop_table('transaction')

