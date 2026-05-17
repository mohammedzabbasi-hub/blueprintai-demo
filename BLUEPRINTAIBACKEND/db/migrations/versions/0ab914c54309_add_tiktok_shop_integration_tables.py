"""add tiktok shop integration tables

Revision ID: 0ab914c54309
Revises: 0001_create_initial_tables
Create Date: 2026-04-18
"""

from alembic import op
import sqlalchemy as sa


revision = "0ab914c54309"
down_revision = "0001_create_initial_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "shop_connections",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("platform", sa.String(length=50), nullable=False, server_default="tiktok"),
        sa.Column("access_token", sa.Text(), nullable=True),
        sa.Column("refresh_token", sa.Text(), nullable=True),
        sa.Column("shop_cipher", sa.String(length=255), nullable=True),
        sa.Column("shop_id_on_platform", sa.String(length=255), nullable=True),
        sa.Column("access_token_expires_at", sa.DateTime(), nullable=True),
        sa.Column("refresh_token_expires_at", sa.DateTime(), nullable=True),
        sa.Column("is_connected", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("raw_payload", sa.Text(), nullable=True),
    )

    op.create_table(
        "shops",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("connection_id", sa.Integer(), sa.ForeignKey("shop_connections.id"), nullable=True),
        sa.Column("shop_name", sa.String(length=255), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("tiktok_shop_id", sa.String(length=255), nullable=True),
        sa.Column("shop_code", sa.String(length=255), nullable=True),
        sa.Column("region", sa.String(length=50), nullable=True),
        sa.Column("currency", sa.String(length=20), nullable=True),
        sa.Column("raw_payload", sa.Text(), nullable=True),
    )

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("shop_id", sa.Integer(), sa.ForeignKey("shops.id"), nullable=False),
        sa.Column("external_id", sa.String(length=255), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("category", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=100), nullable=True),
        sa.Column("price", sa.Float(), nullable=True),
        sa.Column("image_url", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("raw_payload", sa.Text(), nullable=True),
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("shop_id", sa.Integer(), sa.ForeignKey("shops.id"), nullable=False),
        sa.Column("external_id", sa.String(length=255), nullable=True),
        sa.Column("tiktok_order_id", sa.String(length=255), nullable=True),
        sa.Column("buyer_name", sa.String(length=255), nullable=True),
        sa.Column("product_name", sa.String(length=255), nullable=True),
        sa.Column("order_status", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=100), nullable=True),
        sa.Column("currency", sa.String(length=20), nullable=True),
        sa.Column("total_amount", sa.Float(), nullable=True),
        sa.Column("placed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("raw_payload", sa.Text(), nullable=True),
    )

    op.create_table(
        "creatives",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("shop_id", sa.Integer(), sa.ForeignKey("shops.id"), nullable=False),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=True),
        sa.Column("product", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("creator", sa.String(length=255), nullable=False),
        sa.Column("thumbnail", sa.Text(), nullable=True),
        sa.Column("video_url", sa.Text(), nullable=True),
        sa.Column("insight", sa.Text(), nullable=True),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("views", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("likes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("shares", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("clicks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("orders", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("date", sa.String(length=100), nullable=True),
        sa.Column("creator_type", sa.String(length=255), nullable=True),
        sa.Column("creator_archetype", sa.String(length=255), nullable=True),
        sa.Column("ad_type", sa.String(length=255), nullable=True),
        sa.Column("hook_type", sa.String(length=255), nullable=True),
        sa.Column("speaking_style", sa.String(length=255), nullable=True),
        sa.Column("demo_style", sa.String(length=255), nullable=True),
        sa.Column("cta_style", sa.String(length=255), nullable=True),
    )

    op.create_table(
        "metrics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("creative_id", sa.Integer(), sa.ForeignKey("creatives.id"), nullable=False),
        sa.Column("views", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("clicks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("likes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("shares", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("orders", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("ctr", sa.Float(), nullable=True),
        sa.Column("cvr", sa.Float(), nullable=True),
        sa.Column("roas", sa.Float(), nullable=True),
    )

    op.create_table(
        "briefs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("shop_id", sa.Integer(), sa.ForeignKey("shops.id"), nullable=False),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=True),
        sa.Column("product", sa.String(length=255), nullable=False),
        sa.Column("hook", sa.Text(), nullable=False),
        sa.Column("creator_type", sa.String(length=255), nullable=False),
        sa.Column("tone", sa.String(length=255), nullable=True),
        sa.Column("structure", sa.Text(), nullable=True),
        sa.Column("cta", sa.Text(), nullable=True),
        sa.Column("reasoning", sa.Text(), nullable=True),
    )

    op.create_table(
        "recommendations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("shop_id", sa.Integer(), sa.ForeignKey("shops.id"), nullable=False),
        sa.Column("category", sa.String(length=255), nullable=False),
        sa.Column("rec_type", sa.String(length=255), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("confidence", sa.Integer(), nullable=True),
    )

    op.create_table(
        "webhook_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source", sa.String(length=100), nullable=True),
        sa.Column("topic", sa.String(length=255), nullable=True),
        sa.Column("event_type", sa.String(length=255), nullable=True),
        sa.Column("signature", sa.Text(), nullable=True),
        sa.Column("payload", sa.Text(), nullable=True),
        sa.Column("raw_payload", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("is_processed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("processed_at", sa.DateTime(), nullable=True),
        sa.Column("processing_error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "sync_jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("shop_id", sa.Integer(), sa.ForeignKey("shops.id"), nullable=False),
        sa.Column("job_type", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("message", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("sync_jobs")
    op.drop_table("webhook_events")
    op.drop_table("recommendations")
    op.drop_table("briefs")
    op.drop_table("metrics")
    op.drop_table("creatives")
    op.drop_table("orders")
    op.drop_table("products")
    op.drop_table("shops")
    op.drop_table("shop_connections")
