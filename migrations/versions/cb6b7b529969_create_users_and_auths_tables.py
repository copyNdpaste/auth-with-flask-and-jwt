"""create users and auths tables

Revision ID: cb6b7b529969
Revises: 
Create Date: 2021-05-15 11:26:08.258361

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cb6b7b529969"
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
        sa.UniqueConstraint("nickname"),
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
