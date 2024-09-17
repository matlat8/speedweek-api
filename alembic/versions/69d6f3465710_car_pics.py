"""car pics

Revision ID: 69d6f3465710
Revises: ce06b3bd7212
Create Date: 2024-09-15 16:21:35.536650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '69d6f3465710'
down_revision: Union[str, None] = 'ce06b3bd7212'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('car', sa.Column('iracing_car_picture', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('car', 'iracing_car_picture')
    # ### end Alembic commands ###
