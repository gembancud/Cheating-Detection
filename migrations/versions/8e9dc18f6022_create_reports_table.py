"""Create reports table

Revision ID: 8e9dc18f6022
Revises: 
Create Date: 2020-09-24 19:49:08.179982

"""
from alembic import op
import sqlalchemy


# revision identifiers, used by Alembic.
revision = '8e9dc18f6022'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
      'reports',
      sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
      sqlalchemy.Column("confirmed", sqlalchemy.Boolean),
    )


def downgrade():
    op.drop_table('reports')

