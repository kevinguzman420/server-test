"""updated all db tables and relationships

Revision ID: 055dc95667fc
Revises: 3c609c804793
Create Date: 2023-10-16 13:04:04.866064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '055dc95667fc'
down_revision = '3c609c804793'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('subtotal', sa.Float(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('menu_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('total', sa.Float(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('status_order_id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['status_order_id'], ['status_order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_menu_extras',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('extra_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['extra_id'], ['extras.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['order_menu.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('orders_extras')
    op.drop_table('orders')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('orders_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('total', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('rol', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['rol'], ['status_order.id'], name='orders_rol_fkey'),
    sa.PrimaryKeyConstraint('id', name='orders_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('orders_extras',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('extra_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('quantity', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['extra_id'], ['extras.id'], name='orders_extras_extra_id_fkey'),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], name='orders_extras_order_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='orders_extras_pkey')
    )
    op.drop_table('order_menu_extras')
    op.drop_table('order')
    op.drop_table('order_menu')
    op.drop_table('menu')
    # ### end Alembic commands ###