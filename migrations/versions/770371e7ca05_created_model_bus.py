"""created model bus

Revision ID: 770371e7ca05
Revises: 4a85155b8767
Create Date: 2023-11-25 21:48:47.398438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '770371e7ca05'
down_revision = '4a85155b8767'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bus_details', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bus_name', sa.String(length=50), nullable=False))
        batch_op.add_column(sa.Column('departure_time', sa.String(length=50), nullable=False))
        batch_op.alter_column('time_duration',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('bus_details', schema=None) as batch_op:
        batch_op.alter_column('time_duration',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
        batch_op.drop_column('departure_time')
        batch_op.drop_column('bus_name')

    # ### end Alembic commands ###
