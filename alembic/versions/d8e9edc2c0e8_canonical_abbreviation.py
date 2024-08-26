"""create canonical column in abbrevs

Revision ID: d8e9edc2c0e8
Revises: 8e37d049f5d2
Create Date: 2022-10-05 18:00:00.000000

"""
from alembic import op
from adsputils import UTCDateTime, get_date
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd8e9edc2c0e8'
down_revision = '8e37d049f5d2'
branch_labels = None
depends_on = None


def upgrade():

    for table in ['abbrevs', 'abbrevs_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.add_column(sa.Column('canonical', sa.Boolean()))

def downgrade():

    for table in ['abbrevs', 'abbrevs_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.add_column(sa.Column('canonical', sa.Boolean()))

