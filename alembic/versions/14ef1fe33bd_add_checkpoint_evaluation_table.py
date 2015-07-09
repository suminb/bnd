"""Add checkpoint_evaluation table

Revision ID: 14ef1fe33bd
Revises: 3d0a468b38f
Create Date: 2015-07-10 02:35:06.655075

"""

# revision identifiers, used by Alembic.
revision = '14ef1fe33bd'
down_revision = '3d0a468b38f'
branch_labels = None
depends_on = None

from alembic import op
from bnd.models import CheckpointEvaluation


def upgrade():
    # op.create_table(CheckpointEvaluation.__table__)

    # FIXME: Temporary workaround
    from bnd import create_app
    from bnd.models import db
    app = create_app(__name__)
    with app.app_context():
        db.create_all()


def downgrade():
    op.drop_table(CheckpointEvaluation.__tablename__)
