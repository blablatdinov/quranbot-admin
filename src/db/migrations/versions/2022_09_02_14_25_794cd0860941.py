"""Create UserAction.

Revision ID: 794cd0860941
Revises: f6ef093494b4
Create Date: 2022-09-02 14:25:43.925061

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '794cd0860941'
down_revision = 'f6ef093494b4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'user_actions',
        sa.Column('user_action_id', postgresql.UUID(), nullable=False),
        sa.Column('date_time', sa.DateTime(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.chat_id'],
        ),
        sa.PrimaryKeyConstraint('user_action_id'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_actions')
    # ### end Alembic commands ###
