"""Add User Model

Revision ID: 4ebf2be27fe3
Revises: 
Create Date: 2022-06-09 00:35:26.141948

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '4ebf2be27fe3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, default=True),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=True)


def downgrade():
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
