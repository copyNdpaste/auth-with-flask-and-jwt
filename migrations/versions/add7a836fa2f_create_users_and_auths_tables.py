"""create users and auths tables

Revision ID: add7a836fa2f
Revises: 
Create Date: 2021-05-12 23:49:00.698743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "add7a836fa2f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column(
            "id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column("password", sa.String(length=100), nullable=False),
        sa.Column("nickname", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "auth_model",
        sa.Column(
            "id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("identification", sa.String(length=50), nullable=False),
        sa.Column("type", sa.String(length=20), nullable=False),
        sa.Column("verify_code", sa.String(length=50), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=True),
        sa.Column("expired_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("auth_model")
    op.drop_table("users")
