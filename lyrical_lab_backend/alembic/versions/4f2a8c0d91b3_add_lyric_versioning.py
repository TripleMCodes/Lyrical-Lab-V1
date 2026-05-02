"""Postgres-only: add lyric versioning + hashes + optional client_uid idempotency

Revision ID: 4f2a8c0d91b3
Revises: 8ce1cde0e53e
Create Date: 2026-03-05
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# ---- Alembic identifiers ----
revision = "4f2a8c0d91b3"
down_revision = "8ce1cde0e53e"
branch_labels = None
depends_on = None


def upgrade():
    # 0) Enable pgcrypto for sha256 + gen_random_uuid()
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    # 1) Alter existing columns
    op.alter_column(
    "lyrics",
    "client_uid",
    type_=postgresql.UUID(as_uuid=True),
    existing_type=sa.String(length=36),
    existing_nullable=True,
    postgresql_using="client_uid::uuid",
    )
    op.alter_column(
        "lyrics",
        "deleted_at",
        type_=postgresql.TIMESTAMP(timezone=True),
        existing_type=sa.DateTime(),
        existing_nullable=True,
    )

    # Add new versioning columns
    op.add_column(
        "lyrics",
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
    )
    op.add_column(
        "lyrics",
        sa.Column("hash_algo", sa.String(length=20), nullable=False, server_default="sha256"),
    )
    op.add_column(
        "lyrics",
        sa.Column("lyrics_hash", sa.String(length=64), nullable=True),
    )

    # 2) Make timestamps timezone-aware (timestamptz)
    op.alter_column(
        "lyrics",
        "date_created",
        type_=postgresql.TIMESTAMP(timezone=True),
        postgresql_using="date_created AT TIME ZONE 'UTC'",
        existing_nullable=False,
    )
    op.alter_column(
        "lyrics",
        "date_modified",
        type_=postgresql.TIMESTAMP(timezone=True),
        postgresql_using="date_modified AT TIME ZONE 'UTC'",
        existing_nullable=False,
    )

    op.alter_column("lyrics", "date_created", server_default=sa.func.now())
    op.alter_column("lyrics", "date_modified", server_default=sa.func.now())

    op.execute("""
    CREATE OR REPLACE FUNCTION update_date_modified_lyrics()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.date_modified = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER trigger_update_date_modified_lyrics
        BEFORE UPDATE ON lyrics
        FOR EACH ROW
        EXECUTE FUNCTION update_date_modified_lyrics();
    """)

    # 3) Backfill lyrics_hash for existing rows using Postgres sha256 (pgcrypto)
    # Normalize Windows newlines -> \n so hashes are stable across platforms.
    op.execute(sa.text(r"""
        UPDATE lyrics
        SET lyrics_hash = encode(digest(replace(song_lyrics, E'\r\n', E'\n'), 'sha256'), 'hex')
        WHERE lyrics_hash IS NULL
    """))

    # 4) Enforce NOT NULL on lyrics_hash now that it's backfilled
    op.alter_column("lyrics", "lyrics_hash", existing_type=sa.String(length=64), nullable=False)

    # 5) Create versions table (snapshot history)
    op.create_table(
        "lyrics_versions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),

        sa.Column("lyrics_id", sa.Integer(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),

        sa.Column("lyrics", sa.Text(), nullable=False),

        sa.Column("lyrics_hash", sa.String(length=64), nullable=False),
        sa.Column("hash_algo", sa.String(length=20), nullable=False, server_default="sha256"),

        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("note", sa.String(length=120), nullable=True),

        sa.ForeignKeyConstraint(
            ["lyrics_id"],
            ["lyrics.song_id"],
            name="fk_lyrics_versions_lyrics_id",
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("lyrics_id", "version", name="uq_lyrics_versions_lyrics_id_version"),
    )

    op.create_index(
        "ix_lyrics_versions_lyrics_id_created_at",
        "lyrics_versions",
        ["lyrics_id", "created_at"],
        unique=False,
    )


def downgrade():
    # Drop versions
    op.drop_index("ix_lyrics_versions_lyrics_id_created_at", table_name="lyrics_versions")
    op.drop_table("lyrics_versions")

    # Drop versioning columns
    op.drop_column("lyrics", "lyrics_hash")
    op.drop_column("lyrics", "hash_algo")
    op.drop_column("lyrics", "version")

    op.execute("DROP TRIGGER IF EXISTS trigger_update_date_modified_lyrics ON lyrics;")
    op.execute("DROP FUNCTION IF EXISTS update_date_modified_lyrics();")
    op.alter_column("lyrics", "date_created", server_default=None)
    op.alter_column("lyrics", "date_modified", server_default=None)

    # Alter back client_uid
    op.alter_column(
        "lyrics",
        "client_uid",
        type_=sa.String(length=36),
        existing_type=postgresql.UUID(as_uuid=True),
        existing_nullable=True,
    )

    # Alter back deleted_at
    op.alter_column(
        "lyrics",
        "deleted_at",
        type_=sa.DateTime(),
        existing_type=postgresql.TIMESTAMP(timezone=True),
        existing_nullable=True,
    )

    # Revert timestamps to naive timestamp (no tz)
    op.alter_column(
        "lyrics",
        "date_modified",
        type_=postgresql.TIMESTAMP(timezone=False),
        postgresql_using="date_modified::timestamp",
        existing_nullable=False,
    )
    op.alter_column(
        "lyrics",
        "date_created",
        type_=postgresql.TIMESTAMP(timezone=False),
        postgresql_using="date_created::timestamp",
        existing_nullable=False,
    )