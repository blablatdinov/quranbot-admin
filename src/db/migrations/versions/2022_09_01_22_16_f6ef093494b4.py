"""Create MessageModel.

Revision ID: f6ef093494b4
Revises: 5441d86e80de
Create Date: 2022-09-01 22:16:38.016870

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'f6ef093494b4'
down_revision = '5441d86e80de'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'messages',
        sa.Column('message_id', sa.BigInteger(), nullable=False),
        sa.Column('message_json', sa.JSON(), nullable=False),
        sa.Column('is_unknown', sa.Boolean(), nullable=False),
        sa.Column('trigger_message_id', sa.BigInteger(), nullable=True),
        sa.PrimaryKeyConstraint('message_id'),
    )
    op.add_column('users', sa.Column('username', sa.String(), nullable=True))
    op.add_column('users', sa.Column('password_hash', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password_hash')
    op.drop_column('users', 'username')
    op.drop_table('messages')
    # ### end Alembic commands ###
