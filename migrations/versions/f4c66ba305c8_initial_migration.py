"""Initial migration

Revision ID: f4c66ba305c8
Revises: 
Create Date: 2021-10-10 23:36:42.089235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4c66ba305c8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('license',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=255), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=True),
    sa.Column('has_been_used', sa.Boolean(), nullable=False),
    sa.Column('expiration_date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token'),
    sa.UniqueConstraint('value')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('license')
    # ### end Alembic commands ###
