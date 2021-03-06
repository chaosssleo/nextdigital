"""'nav_bar_database'

Revision ID: d5b97f598e77
Revises: 55b585ac242d
Create Date: 2021-04-19 10:24:09.367962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5b97f598e77'
down_revision = '55b585ac242d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('base_navigation',
    sa.Column('page_name', sa.String(length=20), nullable=False),
    sa.Column('page_link', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('page_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('base_navigation')
    # ### end Alembic commands ###
