"""mv completeness details to master

Revision ID: 8e37d049f5d2
Revises: a19fb422743a
Create Date: 2022-10-05 18:00:00.000000

"""
from alembic import op
from adsputils import UTCDateTime, get_date
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8e37d049f5d2'
down_revision = 'a19fb422743a'
branch_labels = None
depends_on = None


def upgrade():

    for table in ['master', 'master_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.add_column(sa.Column('completeness_details', sa.Text()))

    for table in ['titlehistory', 'titlehistory_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.drop_column(column_name='completeness_details')

def downgrade():

    for table in ['titlehistory', 'titlehistory_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.add_column(sa.Column('completeness_details', sa.Text()))

    for table in ['master', 'master_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.drop_column(column_name='completeness_details')
