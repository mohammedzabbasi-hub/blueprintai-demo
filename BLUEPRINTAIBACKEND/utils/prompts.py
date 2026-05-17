def build_video_analysis_user_prompt(
    *,
    video_url: str,
    brand_name: str | None,
    product_name: str | None,
    preprocessed_assets: dict,
) -> str:
    return (
        f"Analyze this TikTok-style creative.\n"
        f"Video URL: {video_url}\n"
        f"Brand: {brand_name or 'Unknown'}\n"
        f"Product: {product_name or 'Unknown'}\n"
        f"Assets: {preprocessed_assets}\n"
        f"Return strict JSON with hook_type, hook_text, humor_style, delivery_style, "
        f"creator_style, promoter_type, subject_focus, pacing, cta_style, strengths, weaknesses, "
        f"transcript_summary, and performance_hypothesis."
    )


def build_brief_prompt(*, brand_name: str | None, product_name: str, winning_creatives: list[dict]) -> str:
    return (
        f"Create a TikTok Shop ad brief.\n"
        f"Brand: {brand_name or 'Unknown'}\n"
        f"Product: {product_name}\n"
        f"Winning creatives: {winning_creatives}\n"
        f"Return strict JSON with brief_title, hook, creator_type, tone, structure, cta, reasoning, "
        f"target_audience, primary_angle, secondary_angle, script, shot_list, dos, donts, references."
    )


def build_recommendations_prompt(*, hooks, creator_types, humor_styles, delivery_styles) -> str:
    return (
        f"Generate recommendations from these creative patterns.\n"
        f"Hooks: {hooks}\n"
        f"Creator Types: {creator_types}\n"
        f"Humor Styles: {humor_styles}\n"
        f"Delivery Styles: {delivery_styles}\n"
        f"Return strict JSON with a recommendations array."
    )
