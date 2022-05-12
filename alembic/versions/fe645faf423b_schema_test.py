"""schema_test

Revision ID: fe645faf423b
Revises: 262d4fc8ae9e
Create Date: 2022-05-12 06:12:57.761194

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import sqlmodel # added


# revision identifiers, used by Alembic.
revision = 'fe645faf423b'
down_revision = '262d4fc8ae9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('testtable',
    sa.Column('test_id', sa.Integer(), nullable=False),
    sa.Column('test_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('test_id'),
    schema='test'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('testtable', schema='test')
    # ### end Alembic commands ###
