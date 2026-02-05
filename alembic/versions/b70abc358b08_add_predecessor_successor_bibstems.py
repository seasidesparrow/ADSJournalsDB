"""add master.masterid foreign key constraint on titlehistory.successor_masterid

Revision ID: b70abc358b08
Revises: 3ada6b0c43aa
Create Date: 2025-08-01 16:00:00.000000

"""
from alembic import op
from adsputils import UTCDateTime, get_date
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b70abc358b08'
down_revision = '3ada6b0c43aa'
branch_labels = None
depends_on = None


def upgrade():

    for table in ['titlehistory', 'titlehistory_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.drop_column("successor_masterid")
            batch_op.add_column(sa.Column("successor_bibstems", sa.String))
            batch_op.add_column(sa.Column("predecessor_bibstems", sa.String))

def downgrade():

    for table in ['titlehistory', 'titlehistory_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.drop_column("predecessor_bibstems")
            batch_op.drop_column("successor_bibstems")
            batch_op.add_column(sa.Column("successor_masterid", sa.Integer))

# end of alembic migration
