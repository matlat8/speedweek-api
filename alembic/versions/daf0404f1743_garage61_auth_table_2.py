"""garage61 auth table 2

Revision ID: daf0404f1743
Revises: 3cf924f12f04
Create Date: 2024-09-19 21:46:33.454259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'daf0404f1743'
down_revision: Union[str, None] = '3cf924f12f04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('garage61_user', sa.Column('garage61_access_token_expires', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('garage61_user', 'garage61_access_token_expires')
    # ### end Alembic commands ###
