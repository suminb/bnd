"""Add a JSON data column to Evaluation

Revision ID: 3d0a468b38f
Revises: 
Create Date: 2015-07-10 01:31:20.578844

"""

# revision identifiers, used by Alembic.
revision = '3d0a468b38f'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

from bnd.models import JsonType

table = 'evaluation'
column = 'data'


def upgrade():
    op.add_column(table, sa.Column(column, JsonType))


def downgrade():
    op.drop_column(table, column)
