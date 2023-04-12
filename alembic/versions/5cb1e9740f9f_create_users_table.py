"""create users table

Revision ID: 5cb1e9740f9f
Revises: 6fb7f92c183a
Create Date: 2023-04-12 17:13:31.759140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cb1e9740f9f'
down_revision = '6fb7f92c183a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Change type of the user_id field wrongly set in the previous revision.
    op.alter_column("posts", column_name="user_id", type_=sa.Integer(),
                    postgresql_using="user_id::integer")

    op.create_table("users",
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )

    # Set the foreing key constraint
    op.create_foreign_key("posts_users_fk", source_table="posts", referent_table="users",
                          local_cols=["user_id"], remote_cols=["id"],
                          ondelete="CASCADE"
                          )


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", "posts")  # remove constraint
    op.drop_table("users")
