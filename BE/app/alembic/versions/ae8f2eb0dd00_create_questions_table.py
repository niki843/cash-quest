"""Create questions table

Revision ID: ae8f2eb0dd00
Revises: 
Create Date: 2025-01-30 14:21:13.968071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae8f2eb0dd00'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'questions',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('value', sa.Integer, nullable=False),
        sa.Column('question', sa.String(1024), nullable=False),
        sa.Column('answer', sa.String(1024), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('questions')
