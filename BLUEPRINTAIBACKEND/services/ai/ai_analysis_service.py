import json
from collections import Counter

from sqlalchemy.orm import Session

from models.video_analysis import VideoAnalysis
from schemas.ai_analysis import ComparisonInsightOut, VideoAnalysisOut, VideoSignalOut
from services.ai.feature_logic import estimate_conversion_score, estimate_engagement_score
from services.ai.llm_client import generate_structured_json
from services.ai.prompts import video_analysis_system_prompt
from services.ai.video_preprocessor import prepare_video_placeholder


FALLBACK_ANALYSIS = {
    "transcript": "",
    "transcript_summary": "Direct-response TikTok style creative with short hook-led structure.",
    "hook_type": "problem-solution",
    "hook_text": "Stop scrolling if you want better results.",
    "humor_style": "light",
    "delivery_style": "fast-paced",
    "creator_style": "ugc creator",
    "promoter_type": "sponsored creator",
    "subject_focus": "product benefit",
    "pacing": "fast",
    "cta_style": "direct",
    "strengths": ["clear hook", "strong platform-native energy"],
    "weaknesses": ["limited proof depth"],
    "performance_hypothesis": "Likely performs because it uses a quick hook and product-first framing.",
}


def analyze_video_url(
    db: Session,
    shop_id: int,
    video_url: str,
    brand_name: str | None,
    product_name: str | None,
) -> VideoAnalysisOut:
    prep = prepare_video_placeholder(video_url)

    user_prompt = json.dumps(
        {
            "video_url": video_url,
            "brand_name": brand_name,
            "product_name": product_name,
            "preprocessed_assets": prep,
            "instruction": "Infer likely creative signals from this TikTok Shop video context. Return strict JSON.",
        }
    )

    result = generate_structured_json(video_analysis_system_prompt(), user_prompt) or FALLBACK_ANALYSIS

    if "raw_text" in result:
        result = FALLBACK_ANALYSIS | {"performance_hypothesis": result["raw_text"]}

    analysis_row = VideoAnalysis(
        shop_id=shop_id,
        source_url=video_url,
        brand_name=brand_name,
        product_name=product_name,
        transcript=result.get("transcript"),
        transcript_summary=result.get("transcript_summary"),
        frames_json=json.dumps(prep.get("frame_paths", [])),
        hook_type=result.get("hook_type"),
        hook_text=result.get("hook_text"),
        humor_style=result.get("humor_style"),
        delivery_style=result.get("delivery_style"),
        creator_style=result.get("creator_style"),
        promoter_type=result.get("promoter_type"),
        subject_focus=result.get("subject_focus"),
        pacing=result.get("pacing"),
        cta_style=result.get("cta_style"),
        performance_hypothesis=result.get("performance_hypothesis"),
        strengths=json.dumps(result.get("strengths", [])),
        weaknesses=json.dumps(result.get("weaknesses", [])),
        structured_output_json=json.dumps(result),
    )
    db.add(analysis_row)
    db.commit()

    return VideoAnalysisOut(
        transcript=result.get("transcript"),
        transcript_summary=result.get("transcript_summary"),
        strengths=result.get("strengths", []),
        weaknesses=result.get("weaknesses", []),
        performance_hypothesis=result.get("performance_hypothesis"),
        signals=VideoSignalOut(
            hook_type=result.get("hook_type"),
            hook_text=result.get("hook_text"),
            humor_style=result.get("humor_style"),
            delivery_style=result.get("delivery_style"),
            creator_style=result.get("creator_style"),
            promoter_type=result.get("promoter_type"),
            subject_focus=result.get("subject_focus"),
            pacing=result.get("pacing"),
            cta_style=result.get("cta_style"),
        ),
        raw=result,
    )


def compare_creatives_for_shop(creatives) -> ComparisonInsightOut:
    hook_counter = Counter([c.hook_type for c in creatives if c.hook_type])
    creator_counter = Counter([c.creator_type for c in creatives if c.creator_type])
    humor_counter = Counter([c.humor_style for c in creatives if c.humor_style])
    delivery_counter = Counter([c.delivery_style for c in creatives if c.delivery_style])
    promoter_counter = Counter(
        [c.promoter_handle or c.creator_archetype for c in creatives if (c.promoter_handle or c.creator_archetype)]
    )

    patterns = []
    for creative in creatives:
        engagement = estimate_engagement_score(
            creative.views or 0,
            creative.likes or 0,
            creative.shares or 0,
            creative.comments or 0,
        )
        conversion = estimate_conversion_score(
            creative.clicks or 0,
            creative.orders or 0,
            creative.views or 0,
        )
        patterns.append(
            f"{creative.title}: engagement_score={engagement}, conversion_score={conversion}, "
            f"hook={creative.hook_type}, creator_type={creative.creator_type}"
        )

    warnings = []
    if not hook_counter:
        warnings.append("Not enough hook metadata yet. Analyze or enrich more creatives.")
    if len(creatives) < 3:
        warnings.append("Comparison is directionally useful but based on a very small sample.")

    return ComparisonInsightOut(
        best_hooks=[name for name, _ in hook_counter.most_common(3)],
        best_creator_types=[name for name, _ in creator_counter.most_common(3)],
        best_humor_styles=[name for name, _ in humor_counter.most_common(3)],
        best_delivery_styles=[name for name, _ in delivery_counter.most_common(3)],
        best_promoter_types=[name for name, _ in promoter_counter.most_common(3)],
        patterns=patterns,
        warnings=warnings,
    )
