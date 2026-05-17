from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from deps import get_db
from models.shop import Shop
from models.creative import Creative

from services.metrics_calculator import calculate_shop_totals
from services.pattern_engine import analyze_patterns, detect_shop_issues
from services.recommendation_engine import generate_recommendations, generate_recommendation_report
from services.brief_generator import generate_briefs_for_shop, generate_brief_report
from services.ai_strategy_writer import write_strategy_summary, build_ai_prompt_payload
from services.insight_scoring import score_all_creatives
from services.gemini_strategy_service import generate_gemini_strategy


router = APIRouter(prefix="/engine", tags=["engine"])


def get_shop_or_404(db: Session, shop_id: int) -> Shop:
    shop = db.query(Shop).filter(Shop.id == shop_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail=f"Shop with id {shop_id} not found")
    return shop


def get_shop_creatives(db: Session, shop_id: int):
    return db.query(Creative).filter(Creative.shop_id == shop_id).all()


@router.get("/analyze-shop")
def analyze_shop(
    shop_id: int = Query(..., description="Shop ID to analyze"),
    db: Session = Depends(get_db),
):
    shop = get_shop_or_404(db, shop_id)
    creatives = get_shop_creatives(db, shop_id)

    return {
        "shop_id": shop.id,
        "shop_name": shop.shop_name or shop.name or f"Shop {shop.id}",
        "total_creatives": len(creatives),
        "totals": calculate_shop_totals(creatives),
        "patterns": analyze_patterns(creatives),
        "issues": detect_shop_issues(creatives),
        "scored_creatives": score_all_creatives(creatives),
        "strategy": write_strategy_summary(creatives),
    }


@router.get("/recommendations")
def engine_recommendations(
    shop_id: int = Query(..., description="Shop ID to generate recommendations for"),
    db: Session = Depends(get_db),
):
    shop = get_shop_or_404(db, shop_id)
    creatives = get_shop_creatives(db, shop_id)

    return {
        "shop_id": shop.id,
        "shop_name": shop.shop_name or shop.name or f"Shop {shop.id}",
        "recommendation_count": len(generate_recommendations(creatives)),
        "report": generate_recommendation_report(creatives),
    }


@router.get("/briefs")
def engine_briefs(
    shop_id: int = Query(..., description="Shop ID to generate briefs for"),
    product_name: str | None = Query(None, description="Optional product name"),
    db: Session = Depends(get_db),
):
    shop = get_shop_or_404(db, shop_id)
    creatives = get_shop_creatives(db, shop_id)

    return {
        "shop_id": shop.id,
        "shop_name": shop.shop_name or shop.name or f"Shop {shop.id}",
        "brief_report": generate_brief_report(creatives, product_name),
        "briefs": generate_briefs_for_shop(creatives, product_name),
    }


@router.get("/strategy-summary")
def engine_strategy_summary(
    shop_id: int = Query(..., description="Shop ID to summarize"),
    db: Session = Depends(get_db),
):
    shop = get_shop_or_404(db, shop_id)
    creatives = get_shop_creatives(db, shop_id)

    return {
        "shop_id": shop.id,
        "shop_name": shop.shop_name or shop.name or f"Shop {shop.id}",
        "strategy": write_strategy_summary(creatives),
    }


@router.get("/ai-payload")
def engine_ai_payload(
    shop_id: int = Query(..., description="Shop ID to prepare AI payload for"),
    product_name: str | None = Query(None, description="Optional product name"),
    db: Session = Depends(get_db),
):
    shop = get_shop_or_404(db, shop_id)
    creatives = get_shop_creatives(db, shop_id)

    return {
        "shop_id": shop.id,
        "shop_name": shop.shop_name or shop.name or f"Shop {shop.id}",
        "ai_payload": build_ai_prompt_payload(creatives, product_name),
    }


@router.get("/gemini-strategy")
def engine_gemini_strategy(
    shop_id: int = Query(..., description="Shop ID to analyze with Gemini"),
    product_name: str | None = Query(None, description="Optional product name"),
    db: Session = Depends(get_db),
):
    shop = get_shop_or_404(db, shop_id)
    creatives = get_shop_creatives(db, shop_id)

    try:
        result = generate_gemini_strategy(creatives, product_name)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return {
        "shop_id": shop.id,
        "shop_name": shop.shop_name or shop.name or f"Shop {shop.id}",
        "result": result,
    }
