"""create deprecated column in master

Revision ID: 3ada6b0c43aa
Revises: d8e9edc2c0e8
Create Date: 2022-10-05 18:00:00.000000

"""
from alembic import op
from adsputils import UTCDateTime, get_date
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3ada6b0c43aa'
down_revision = 'd8e9edc2c0e8'
branch_labels = None
depends_on = None


def upgrade():

    for table in ['master', 'master_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.add_column(sa.Column('deprecated', sa.Boolean(), default=False))

def downgrade():

    for table in ['master', 'master_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.drop_column(column_name='deprecated')


