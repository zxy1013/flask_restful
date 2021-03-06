"""empty message

Revision ID: 89a4dfc9e64c
Revises: 8d7d7d756d97
Create Date: 2021-04-18 16:46:28.906294

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89a4dfc9e64c'
down_revision = '8d7d7d756d97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friend',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('fid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['fid'], ['user.id'], ),
    sa.ForeignKeyConstraint(['uid'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('email', sa.String(length=100), nullable=True))
    op.add_column('user', sa.Column('icon', sa.String(length=150), nullable=True))
    op.add_column('user', sa.Column('isdelete', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('phone', sa.String(length=11), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'phone')
    op.drop_column('user', 'isdelete')
    op.drop_column('user', 'icon')
    op.drop_column('user', 'email')
    op.drop_table('friend')
    # ### end Alembic commands ###
