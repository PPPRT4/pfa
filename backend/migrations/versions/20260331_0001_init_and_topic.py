"""create base tables and ensure notes.topic exists

Revision ID: 20260331_0001
Revises:
Create Date: 2026-03-31
"""

from alembic import op
import sqlalchemy as sa


revision = "20260331_0001"
down_revision = None
branch_labels = None
depends_on = None


def _has_table(inspector: sa.Inspector, table_name: str) -> bool:
    return table_name in inspector.get_table_names()


def _has_column(inspector: sa.Inspector, table_name: str, column_name: str) -> bool:
    cols = inspector.get_columns(table_name)
    return any(col["name"] == column_name for col in cols)


def _has_index(inspector: sa.Inspector, table_name: str, index_name: str) -> bool:
    return any(idx.get("name") == index_name for idx in inspector.get_indexes(table_name))


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _has_table(inspector, "users"):
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("username", sa.String(), nullable=False),
            sa.Column("email", sa.String(), nullable=False),
            sa.Column("hashed_password", sa.String(), nullable=False),
        )

    inspector = sa.inspect(bind)
    if not _has_index(inspector, "users", "ix_users_id"):
        op.create_index("ix_users_id", "users", ["id"], unique=False)
    if not _has_index(inspector, "users", "ix_users_username"):
        op.create_index("ix_users_username", "users", ["username"], unique=False)
    if not _has_index(inspector, "users", "ix_users_email"):
        op.create_index("ix_users_email", "users", ["email"], unique=True)

    inspector = sa.inspect(bind)
    if not _has_table(inspector, "notes"):
        op.create_table(
            "notes",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("title", sa.String(), nullable=False),
            sa.Column("content", sa.String(), nullable=False),
            sa.Column("topic", sa.String(), nullable=False, server_default="Idea"),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        )

    inspector = sa.inspect(bind)
    if not _has_index(inspector, "notes", "ix_notes_id"):
        op.create_index("ix_notes_id", "notes", ["id"], unique=False)

    inspector = sa.inspect(bind)
    if _has_table(inspector, "notes") and not _has_column(inspector, "notes", "topic"):
        op.add_column(
            "notes",
            sa.Column("topic", sa.String(), nullable=False, server_default="Idea"),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if _has_table(inspector, "notes") and _has_column(inspector, "notes", "topic"):
        op.drop_column("notes", "topic")
