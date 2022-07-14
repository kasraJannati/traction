# flake8: noqa
"""v1-holder-credential

Revision ID: ac386d404ddf
Revises: 59e15b37dab5
Create Date: 2022-07-07 10:42:24.922102

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ac386d404ddf"
down_revision = "59e15b37dab5"
branch_labels = None
depends_on = None

create_timeline_func = """CREATE OR REPLACE FUNCTION holder_credential_timeline_func() RETURNS trigger AS $body$
    BEGIN
        IF NEW.status IS DISTINCT FROM OLD.status OR NEW.state IS DISTINCT FROM OLD.state THEN
            INSERT INTO "timeline" ( "item_id", "status", "state", "error_status_detail" )
            VALUES(NEW."holder_credential_id", NEW."status", NEW."state", NEW."error_status_detail");
            RETURN NEW;
        END IF;
        RETURN null;
    END;
    $body$ LANGUAGE plpgsql
"""

drop_timeline_func = """DROP FUNCTION holder_credential_timeline_func"""

create_timeline_trigger = """CREATE TRIGGER holder_credential_timeline_trigger
AFTER INSERT OR UPDATE OF status, state ON holder_credential
FOR EACH ROW EXECUTE PROCEDURE holder_credential_timeline_func();"""

drop_timeline_trigger = (
    """DROP TRIGGER holder_credential_timeline_trigger ON holder_credential"""
)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "holder_credential",
        sa.Column(
            "holder_credential_id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("tenant_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("contact_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("status", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("state", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "external_reference_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.Column("tags", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("deleted", sa.Boolean(), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False),
        sa.Column(
            "revocation_comment", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.Column("thread_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column(
            "credential_exchange_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.Column("connection_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("schema_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("cred_def_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("credential_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("revoc_reg_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("revocation_id", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("error_status_detail", sa.VARCHAR(), nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["contact_id"],
            ["contact.contact_id"],
        ),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["tenant.id"],
        ),
        sa.PrimaryKeyConstraint("holder_credential_id"),
    )
    op.create_index(
        op.f("ix_holder_credential_contact_id"),
        "holder_credential",
        ["contact_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_holder_credential_tenant_id"),
        "holder_credential",
        ["tenant_id"],
        unique=False,
    )
    # ### end Alembic commands ###
    op.execute(create_timeline_func)
    op.execute(create_timeline_trigger)


def downgrade():
    op.execute(drop_timeline_trigger)
    op.execute(drop_timeline_func)
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_holder_credential_tenant_id"), table_name="holder_credential"
    )
    op.drop_index(
        op.f("ix_holder_credential_contact_id"), table_name="holder_credential"
    )
    op.drop_table("holder_credential")
    # ### end Alembic commands ###