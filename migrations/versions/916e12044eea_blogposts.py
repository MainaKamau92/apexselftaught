"""blogposts

Revision ID: 916e12044eea
Revises: cf401f3b026e
Create Date: 2019-02-18 01:54:31.857672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '916e12044eea'
down_revision = 'cf401f3b026e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blogposts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'blogposts', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'blogposts', type_='foreignkey')
    op.drop_column('blogposts', 'user_id')
    # ### end Alembic commands ###
