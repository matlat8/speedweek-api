"""cascade delete on leagues

Revision ID: e2063300ab3f
Revises: 9cb8fc633e8a
Create Date: 2024-09-05 19:47:34.925706

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2063300ab3f'
down_revision: Union[str, None] = '9cb8fc633e8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('season_league_id_fkey', 'season', type_='foreignkey')
    op.create_foreign_key(None, 'season', 'league', ['league_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'season', type_='foreignkey')
    op.create_foreign_key('season_league_id_fkey', 'season', 'league', ['league_id'], ['id'])
    # ### end Alembic commands ###
