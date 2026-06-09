"""add master.masterid foreign key constraint on titlehistory.successor_masterid

Revision ID: 883ea1acd79f
Revises: b70abc358b08
Create Date: 2026-06-09 16:00:00.000000

"""
from alembic import op
from adsputils import UTCDateTime, get_date
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '883ea1acd79f'
down_revision = 'b70abc358b08'
branch_labels = None
depends_on = None


def upgrade():

    for table in ['titlehistory', 'titlehistory_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.add_column(sa.Column("successor_issns", sa.String))
            batch_op.add_column(sa.Column("predecessor_issns", sa.String))
            batch_op.add_column(sa.Column("successor_codens", sa.String))
            batch_op.add_column(sa.Column("predecessor_codens", sa.String))

def downgrade():

    for table in ['titlehistory', 'titlehistory_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.drop_column("predecessor_codens")
            batch_op.drop_column("successor_codens")
            batch_op.drop_column("predecessor_issns")
            batch_op.drop_column("successor_issns")

# end of alembic migration
