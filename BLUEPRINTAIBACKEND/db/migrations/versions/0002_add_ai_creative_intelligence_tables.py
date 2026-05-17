"""add ai creative intelligence tables and fields

Revision ID: 0002_add_ai_creative_intelligence_tables
Revises: 0ab914c54309
Create Date: 2026-04-18
"""

from alembic import op
import sqlalchemy as sa


revision = "0002_add_ai_creative_intelligence_tables"
down_revision = "0ab914c54309"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("creatives", sa.Column("source_platform", sa.String(length=100), nullable=True))
    op.add_column("creatives", sa.Column("transcript", sa.Text(), nullable=True))
    op.add_column("creatives", sa.Column("transcript_summary", sa.Text(), nullable=True))
    op.add_column("creatives", sa.Column("promoter_handle", sa.String(length=255), nullable=True))
    op.add_column("creatives", sa.Column("humor_style", sa.String(length=255), nullable=True))
    op.add_column("creatives", sa.Column("delivery_style", sa.String(length=255), nullable=True))
    op.add_column("creatives", sa.Column("hook_text", sa.Text(), nullable=True))
    op.add_column("creatives", sa.Column("primary_subject", sa.String(length=255), nullable=True))
    op.add_column("creatives", sa.Column("visual_style", sa.String(length=255), nullable=True))
    op.add_column("creatives", sa.Column("pacing", sa.String(length=255), nullable=True))
    op.add_column("creatives", sa.Column("text_overlay_style", sa.String(length=255), nullable=True))
    op.add_column("creatives", sa.Column("winning_reason", sa.Text(), nullable=True))
    op.add_column("creatives", sa.Column("ai_summary", sa.Text(), nullable=True))
    op.add_column("creatives", sa.Column("raw_ai_json", sa.Text(), nullable=True))
    op.add_column("creatives", sa.Column("engagement_score", sa.Float(), nullable=True))
    op.add_column("creatives", sa.Column("conversion_score", sa.Float(), nullable=True))
    op.add_column("creatives", sa.Column("comments", sa.Integer(), nullable=False, server_default="0"))

    op.add_column("briefs", sa.Column("brief_title", sa.String(length=255), nullable=True))
    op.add_column("briefs", sa.Column("target_audience", sa.Text(), nullable=True))
    op.add_column("briefs", sa.Column("primary_angle", sa.Text(), nullable=True))
    op.add_column("briefs", sa.Column("secondary_angle", sa.Text(), nullable=True))
    op.add_column("briefs", sa.Column("script", sa.Text(), nullable=True))
    op.add_column("briefs", sa.Column("shot_list", sa.Text(), nullable=True))
    op.add_column("briefs", sa.Column("dos", sa.Text(), nullable=True))
    op.add_column("briefs", sa.Column("donts", sa.Text(), nullable=True))
    op.add_column("briefs", sa.Column("references", sa.Text(), nullable=True))
    op.add_column("briefs", sa.Column("raw_ai_json", sa.Text(), nullable=True))

    op.add_column("recommendations", sa.Column("product_name", sa.String(length=255), nullable=True))
    op.add_column("recommendations", sa.Column("evidence", sa.Text(), nullable=True))
    op.add_column("recommendations", sa.Column("action", sa.Text(), nullable=True))
    op.add_column("recommendations", sa.Column("priority", sa.String(length=50), nullable=True))
    op.add_column("recommendations", sa.Column("based_on_creative_ids", sa.Text(), nullable=True))

    op.create_table(
        "video_analyses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("shop_id", sa.Integer(), sa.ForeignKey("shops.id"), nullable=False),
        sa.Column("creative_id", sa.Integer(), sa.ForeignKey("creatives.id"), nullable=True),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("source_platform", sa.String(length=100), nullable=False, server_default="tiktok"),
        sa.Column("brand_name", sa.String(length=255), nullable=True),
        sa.Column("product_name", sa.String(length=255), nullable=True),
        sa.Column("transcript", sa.Text(), nullable=True),
        sa.Column("transcript_summary", sa.Text(), nullable=True),
        sa.Column("frames_json", sa.Text(), nullable=True),
        sa.Column("hook_type", sa.String(length=255), nullable=True),
        sa.Column("hook_text", sa.Text(), nullable=True),
        sa.Column("humor_style", sa.String(length=255), nullable=True),
        sa.Column("delivery_style", sa.String(length=255), nullable=True),
        sa.Column("creator_style", sa.String(length=255), nullable=True),
        sa.Column("promoter_type", sa.String(length=255), nullable=True),
        sa.Column("subject_focus", sa.String(length=255), nullable=True),
        sa.Column("pacing", sa.String(length=255), nullable=True),
        sa.Column("cta_style", sa.String(length=255), nullable=True),
        sa.Column("performance_hypothesis", sa.Text(), nullable=True),
        sa.Column("strengths", sa.Text(), nullable=True),
        sa.Column("weaknesses", sa.Text(), nullable=True),
        sa.Column("structured_output_json", sa.Text(), nullable=True),
    )

    op.create_index("ix_video_analyses_id", "video_analyses", ["id"])
    op.create_index("ix_video_analyses_shop_id", "video_analyses", ["shop_id"])
    op.create_index("ix_video_analyses_creative_id", "video_analyses", ["creative_id"])


def downgrade() -> None:
    op.drop_index("ix_video_analyses_creative_id", table_name="video_analyses")
    op.drop_index("ix_video_analyses_shop_id", table_name="video_analyses")
    op.drop_index("ix_video_analyses_id", table_name="video_analyses")
    op.drop_table("video_analyses")

    op.drop_column("recommendations", "based_on_creative_ids")
    op.drop_column("recommendations", "priority")
    op.drop_column("recommendations", "action")
    op.drop_column("recommendations", "evidence")
    op.drop_column("recommendations", "product_name")

    op.drop_column("briefs", "raw_ai_json")
    op.drop_column("briefs", "references")
    op.drop_column("briefs", "donts")
    op.drop_column("briefs", "dos")
    op.drop_column("briefs", "shot_list")
    op.drop_column("briefs", "script")
    op.drop_column("briefs", "secondary_angle")
    op.drop_column("briefs", "primary_angle")
    op.drop_column("briefs", "target_audience")
    op.drop_column("briefs", "brief_title")

    op.drop_column("creatives", "comments")
    op.drop_column("creatives", "conversion_score")
    op.drop_column("creatives", "engagement_score")
    op.drop_column("creatives", "raw_ai_json")
    op.drop_column("creatives", "ai_summary")
    op.drop_column("creatives", "winning_reason")
    op.drop_column("creatives", "text_overlay_style")
    op.drop_column("creatives", "pacing")
    op.drop_column("creatives", "visual_style")
    op.drop_column("creatives", "primary_subject")
    op.drop_column("creatives", "hook_text")
    op.drop_column("creatives", "delivery_style")
    op.drop_column("creatives", "humor_style")
    op.drop_column("creatives", "promoter_handle")
    op.drop_column("creatives", "transcript_summary")
    op.drop_column("creatives", "transcript")
    op.drop_column("creatives", "source_platform")
