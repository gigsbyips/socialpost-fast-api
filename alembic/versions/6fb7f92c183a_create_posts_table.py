"""create posts table

Revision ID: 6fb7f92c183a
Revises: 
Create Date: 2023-04-12 17:05:36.983390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fb7f92c183a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
        op.create_table("posts", 
        sa.Column('id', sa.Integer(), primary_key=True), 
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('visibility', sa.String(), nullable=False, server_default='public'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
        sa.Column('user_id', sa.String(), nullable=False)) # Intentionally set to wrong Type.
        
def downgrade() -> None:
    op.drop_table("posts")
