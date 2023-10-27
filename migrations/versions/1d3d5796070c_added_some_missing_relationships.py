"""added some missing relationships

Revision ID: 1d3d5796070c
Revises: 055dc95667fc
Create Date: 2023-10-16 13:14:42.233069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d3d5796070c'
down_revision = '055dc95667fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_menu', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'order', ['order_id'], ['id'])
        batch_op.create_foreign_key(None, 'menu', ['menu_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_menu', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###