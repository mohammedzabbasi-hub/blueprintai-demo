from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import inspect, text
from db.database import engine
from deps import get_current_active_user
from models.user import User
from routes.login import DEMO_ACCOUNTS
from datetime import datetime

router = APIRouter(prefix="/personalized", tags=["personalized"])


class SaveCreativeRequest(BaseModel):
    shop_id: int
    title: str | None = None
    product: str | None = None
    creator: str | None = None
    video_url: str | None = None
    thumbnail: str | None = None
    insight: str | None = None
    transcript: str | None = None
    transcript_summary: str | None = None
    hook_type: str | None = None
    creator_type: str | None = None
    humor_style: str | None = None
    delivery_style: str | None = None
    score: float | None = None


def table_exists(table_name):
    return table_name in inspect(engine).get_table_names()


def columns(table_name):
    if not table_exists(table_name):
        return set()
    return {c["name"] for c in inspect(engine).get_columns(table_name)}


def insert_dynamic(conn, table_name, values):
    actual_cols = columns(table_name)
    filtered = {k: v for k, v in values.items() if k in actual_cols and v is not None}

    if not filtered:
        raise HTTPException(status_code=500, detail=f"No matching columns for {table_name}")

    col_sql = ", ".join(filtered.keys())
    bind_sql = ", ".join([f":{k}" for k in filtered.keys()])

    result = conn.execute(
        text(f"INSERT INTO {table_name} ({col_sql}) VALUES ({bind_sql})"),
        filtered,
    )
    return result.lastrowid


def fetch_all(conn, sql, params=None):
    return [dict(row) for row in conn.execute(text(sql), params or {}).mappings().all()]


def verify_shop_access(conn, shop_id: int, current_user: User):
    shop = conn.execute(
        text("SELECT id, user_id, tiktok_shop_id FROM shops WHERE id = :shop_id LIMIT 1"),
        {"shop_id": shop_id},
    ).mappings().first()

    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    email = str(getattr(current_user, "email", "") or "").lower()
    demo_account = DEMO_ACCOUNTS.get(email)
    is_allowed_demo_shop = (
        demo_account is not None
        and shop_id in demo_account["shop_ids"]
        and str(shop.get("tiktok_shop_id") or "").startswith("demo_shop_")
    )

    if is_allowed_demo_shop:
        return shop

    if shop["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have access to this shop")

    return shop


@router.get("/shop-state")
def get_shop_state(shop_id: int):
    with engine.begin() as conn:
        creatives_count = 0
        recommendations_count = 0
        briefs_count = 0
        activity_count = 0
        creators_count = 0

        if table_exists("creatives") and "shop_id" in columns("creatives"):
            creatives_count = conn.execute(
                text("SELECT COUNT(*) FROM creatives WHERE shop_id = :shop_id"),
                {"shop_id": shop_id},
            ).scalar() or 0

        if table_exists("recommendations") and "shop_id" in columns("recommendations"):
            recommendations_count = conn.execute(
                text("SELECT COUNT(*) FROM recommendations WHERE shop_id = :shop_id"),
                {"shop_id": shop_id},
            ).scalar() or 0

        if table_exists("briefs") and "shop_id" in columns("briefs"):
            briefs_count = conn.execute(
                text("SELECT COUNT(*) FROM briefs WHERE shop_id = :shop_id"),
                {"shop_id": shop_id},
            ).scalar() or 0

        if table_exists("activity_logs") and "shop_id" in columns("activity_logs"):
            activity_count = conn.execute(
                text("SELECT COUNT(*) FROM activity_logs WHERE shop_id = :shop_id"),
                {"shop_id": shop_id},
            ).scalar() or 0

        creator_cols = columns("creators")
        if table_exists("creators") and "shop_id" in creator_cols:
            creators_count = conn.execute(
                text("SELECT COUNT(*) FROM creators WHERE shop_id = :shop_id"),
                {"shop_id": shop_id},
            ).scalar() or 0
        elif table_exists("creators") and "brand_id" in creator_cols:
            creators_count = conn.execute(
                text("SELECT COUNT(*) FROM creators WHERE brand_id = :shop_id"),
                {"shop_id": shop_id},
            ).scalar() or 0

    return {
        "shop_id": shop_id,
        "has_data": any([creatives_count, recommendations_count, briefs_count, activity_count, creators_count]),
        "counts": {
            "creatives": creatives_count,
            "recommendations": recommendations_count,
            "briefs": briefs_count,
            "activity": activity_count,
            "creators": creators_count,
        },
    }


@router.get("/creatives")
def get_personalized_creatives(
    shop_id: int,
    current_user: User = Depends(get_current_active_user),
):
    if not table_exists("creatives") or "shop_id" not in columns("creatives"):
        return []

    with engine.begin() as conn:
        verify_shop_access(conn, shop_id, current_user)

        rows = fetch_all(
            conn,
            "SELECT * FROM creatives WHERE shop_id = :shop_id ORDER BY id DESC",
            {"shop_id": shop_id},
        )

    return rows


@router.get("/creatives/{creative_id}")
def get_personalized_creative(
    creative_id: int,
    shop_id: int,
    current_user: User = Depends(get_current_active_user),
):
    if not table_exists("creatives") or "shop_id" not in columns("creatives"):
        raise HTTPException(status_code=404, detail="Creative not found")

    with engine.begin() as conn:
        verify_shop_access(conn, shop_id, current_user)

        row = conn.execute(
            text("""
                SELECT * FROM creatives
                WHERE id = :creative_id AND shop_id = :shop_id
                LIMIT 1
            """),
            {"creative_id": creative_id, "shop_id": shop_id},
        ).mappings().first()

    if not row:
        raise HTTPException(status_code=404, detail="Creative not found")

    return dict(row)


@router.post("/creatives")
def save_personalized_creative(payload: SaveCreativeRequest):
    if not table_exists("creatives"):
        raise HTTPException(status_code=500, detail="Creatives table does not exist.")

    now = datetime.utcnow().isoformat()

    with engine.begin() as conn:
        creative_id = insert_dynamic(conn, "creatives", {
            "shop_id": payload.shop_id,
            "title": payload.title or "Uploaded Creative",
            "product": payload.product,
            "creator": payload.creator or "Uploaded by user",
            "video_url": payload.video_url,
            "thumbnail": payload.thumbnail,
            "insight": payload.insight,
            "transcript": payload.transcript,
            "transcript_summary": payload.transcript_summary,
            "hook_type": payload.hook_type,
            "creator_type": payload.creator_type,
            "humor_style": payload.humor_style,
            "delivery_style": payload.delivery_style,
            "creative_score": payload.score,
            "score": payload.score,
            "created_at": now,
        })

        if table_exists("activity_logs"):
            try:
                insert_dynamic(conn, "activity_logs", {
                    "shop_id": payload.shop_id,
                    "user_email": "system",
                    "user_name": "System",
                    "activity_type": "creative_upload",
                    "title": "Creative saved",
                    "description": payload.title or "Uploaded Creative",
                    "created_at": now,
                })
            except Exception:
                pass

    return {
        "success": True,
        "creative_id": creative_id,
        "shop_id": payload.shop_id,
    }


@router.get("/dashboard")
def personalized_dashboard(shop_id: int):
    state = get_shop_state(shop_id)
    return {
        "shop_id": shop_id,
        "counts": state["counts"],
        "has_data": state["has_data"],
    }


@router.get("/recommendations")
def personalized_recommendations(shop_id: int):
    if not table_exists("recommendations") or "shop_id" not in columns("recommendations"):
        return []

    with engine.begin() as conn:
        return fetch_all(
            conn,
            "SELECT * FROM recommendations WHERE shop_id = :shop_id ORDER BY id DESC",
            {"shop_id": shop_id},
        )


@router.get("/briefs")
def personalized_briefs(shop_id: int):
    if not table_exists("briefs") or "shop_id" not in columns("briefs"):
        return []

    with engine.begin() as conn:
        return fetch_all(
            conn,
            "SELECT * FROM briefs WHERE shop_id = :shop_id ORDER BY id DESC",
            {"shop_id": shop_id},
        )


@router.get("/creators")
def personalized_creators(shop_id: int):
    creator_cols = columns("creators")
    if not table_exists("creators"):
        return []

    with engine.begin() as conn:
        if "shop_id" in creator_cols:
            return fetch_all(
                conn,
                "SELECT * FROM creators WHERE shop_id = :shop_id ORDER BY id DESC",
                {"shop_id": shop_id},
            )

        if "brand_id" not in creator_cols:
            return []

        return fetch_all(
            conn,
            "SELECT * FROM creators WHERE brand_id = :shop_id ORDER BY id DESC",
            {"shop_id": shop_id},
        )
