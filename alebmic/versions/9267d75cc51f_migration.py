"""migration

Revision ID: 9267d75cc51f
Revises: 
Create Date: 2022-07-12 18:44:52.692278

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


# revision identifiers, used by Alembic.
revision = '9267d75cc51f'
down_revision = None
branch_labels = None
depends_on = None


def create_cleanings_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, unique=True, index=True),
        sa.Column("hashed_password", sa.String, nullable=True),
        sa.Column("is_active", sa.Boolean, default=True),
        relationship("Item", back_populates="owner")
    )
    op.create_table(
        "items",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("title", sa.String, index=True),
        sa.Column("description", sa.Text, index=True),
        sa.Column("owned_id", sa.Integer, ForeignKey("users.id")),
        relationship("User", back_populates="items")
    )


def upgrade() -> None:
    create_cleanings_table()


def downgrade() -> None:
    pass
