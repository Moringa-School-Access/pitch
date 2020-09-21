"""image migration

Revision ID: 498fc9fb9732
Revises: d636fd707304
Create Date: 2020-09-22 00:40:35.020451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '498fc9fb9732'
down_revision = 'd636fd707304'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password_secure')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_secure', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
