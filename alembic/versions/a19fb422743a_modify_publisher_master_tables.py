"""modify publisher master tables

Revision ID: a19fb422743a
Revises: a476d887b4e1
Create Date: 2022-10-05 18:00:00.000000

"""
from alembic import op
from adsputils import UTCDateTime, get_date
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a19fb422743a'
down_revision = 'a476d887b4e1'
branch_labels = None
depends_on = None


def upgrade():

    for table in ['publisher', 'publisher_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.alter_column(column_name='pubname', new_column_name='pubabbrev')
            batch_op.add_column(sa.Column('pubfullname', sa.String()))

    for table in ['master', 'master_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.alter_column(column_name='complete', new_column_name='completeness_fraction')

    for table in ['titlehistory', 'titlehistory_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.alter_column(column_name='complete', new_column_name='completeness_details')

def downgrade():

    for table in ['titlehistory', 'titlehistory_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.alter_column(column_name='completeness_details', new_column_name='complete')

    for table in ['master', 'master_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.alter_column(column_name='completeness_fraction', new_column_name='complete')

    for table in ['publisher', 'publisher_hist']:
        with op.batch_alter_table(table) as batch_op:
            batch_op.drop_column('pubfullname')
            batch_op.alter_column(column_name='pubabbrev', new_column_name='pubname')
