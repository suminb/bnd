"""add announcement table

Revision ID: 2059358d0f
Revises: 14ef1fe33bd
Create Date: 2015-08-01 14:53:05.895942

"""

# revision identifiers, used by Alembic.
revision = '2059358d0f'
down_revision = '14ef1fe33bd'
branch_labels = None
depends_on = None

from alembic import op
from bnd.models import Announcement


def upgrade():
    # FIXME: Temporary workaround
    from bnd import create_app
    from bnd.models import db
    app = create_app(__name__)
    with app.app_context():
        db.create_all()


def downgrade():
    op.drop_table(Announcement.__tablename__)
