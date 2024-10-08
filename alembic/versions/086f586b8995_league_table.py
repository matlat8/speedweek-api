"""league table

Revision ID: 086f586b8995
Revises: 7c2a65f431c6
Create Date: 2024-08-11 19:27:17.115912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '086f586b8995'
down_revision: Union[str, None] = '7c2a65f431c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('league',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('owner_id', sa.UUID(), nullable=False),
    sa.Column('discord_guild_id', sa.String(), nullable=True),
    sa.Column('visibility', sa.Boolean(), nullable=False),
    sa.Column('invite_token', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_league_id'), 'league', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_league_id'), table_name='league')
    op.drop_table('league')
    # ### end Alembic commands ###
