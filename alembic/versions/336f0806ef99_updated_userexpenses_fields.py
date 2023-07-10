"""updated userexpenses fields

Revision ID: 336f0806ef99
Revises: bb6240e03dcc
Create Date: 2023-07-10 22:33:27.274769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '336f0806ef99'
down_revision = 'bb6240e03dcc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_expense_group', table_name='expense')
    op.drop_index('ix_expense_user', table_name='expense')
    op.drop_table('expense')
    op.drop_index('ix_expenseuser_user', table_name='expenseuser')
    op.drop_table('expenseuser')
    op.drop_index('ix_user_email', table_name='user')
    op.drop_index('ix_user_id', table_name='user')
    op.drop_index('ix_user_phone_number', table_name='user')
    op.drop_index('ix_group_id', table_name='group')
    op.drop_table('groupmember')
    op.drop_table('group')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groupmember',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('group_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], name='groupmember_group_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='groupmember_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='groupmember_pkey')
    )
    op.create_table('group',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='group_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_group_id', 'group', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('phone_number', sa.VARCHAR(length=14), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_user_phone_number', 'user', ['phone_number'], unique=False)
    op.create_index('ix_user_id', 'user', ['id'], unique=False)
    op.create_index('ix_user_email', 'user', ['email'], unique=False)
    op.create_table('expenseuser',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('amount_paid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('amount_owed', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('net_balance', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('user', sa.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user'], ['user.id'], name='expenseuser_user_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='expenseuser_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='expenseuser_pkey')
    )
    op.create_index('ix_expenseuser_user', 'expenseuser', ['user'], unique=False)
    op.create_table('expense',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('total_amount', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('user', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('group', sa.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['group'], ['group.id'], name='expense_group_fkey'),
    sa.ForeignKeyConstraint(['user'], ['user.id'], name='expense_user_fkey'),
    sa.PrimaryKeyConstraint('id', name='expense_pkey')
    )
    op.create_index('ix_expense_user', 'expense', ['user'], unique=False)
    op.create_index('ix_expense_group', 'expense', ['group'], unique=False)
    # ### end Alembic commands ###