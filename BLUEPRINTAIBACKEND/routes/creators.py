from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from models.creator import Creator
from schemas.creator import CreatorCreate, CreatorOut, CreatorUpdate

try:
    from db.database import SessionLocal
except ModuleNotFoundError:
    from app.db.database import SessionLocal


router = APIRouter(prefix="/creators", tags=["Creators"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def calculate_creator_score(creator: Creator) -> int:
    views_score = min((creator.total_views or 0) / 100000, 30)

    engagement = (
        (creator.total_likes or 0)
        + (creator.total_comments or 0)
        + (creator.total_shares or 0)
    )

    engagement_score = min(engagement / 10000, 25)
    revenue_score = min((creator.total_revenue or 0) / 1000, 30)
    consistency_score = min((creator.total_videos or 0) * 2, 15)

    return round(views_score + engagement_score + revenue_score + consistency_score)


@router.post("/", response_model=CreatorOut)
def create_creator(creator_data: CreatorCreate, db: Session = Depends(get_db)):
    creator = Creator(**creator_data.model_dump())
    db.add(creator)
    db.commit()
    db.refresh(creator)
    return creator


@router.get("/", response_model=list[CreatorOut])
def get_creators(
    shop_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Creator)

    if shop_id is not None:
        query = query.filter(Creator.brand_id == shop_id)

    return query.order_by(Creator.total_revenue.desc()).all()


@router.get("/compare")
def compare_creators(
    shop_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Creator)

    if shop_id is not None:
        query = query.filter(Creator.brand_id == shop_id)

    creators = query.all()

    ranked_creators = []

    for creator in creators:
        ranked_creators.append(
            {
                "id": creator.id,
                "name": creator.name,
                "tiktok_handle": creator.tiktok_handle,
                "follower_count": creator.follower_count,
                "total_videos": creator.total_videos,
                "total_views": creator.total_views,
                "total_likes": creator.total_likes,
                "total_comments": creator.total_comments,
                "total_shares": creator.total_shares,
                "total_conversions": creator.total_conversions,
                "total_revenue": creator.total_revenue,
                "performance_score": calculate_creator_score(creator),
            }
        )

    ranked_creators.sort(
        key=lambda creator: creator["performance_score"],
        reverse=True,
    )

    best_creator = ranked_creators[0] if ranked_creators else None

    return {
        "creators": ranked_creators,
        "best_creator": best_creator,
        "summary": (
            f"{best_creator['name']} is currently the strongest creator for this shop based on views, engagement, revenue, and consistency."
            if best_creator
            else "No creators have been added for this shop yet."
        ),
    }


@router.get("/{creator_id}", response_model=CreatorOut)
def get_creator(creator_id: int, db: Session = Depends(get_db)):
    creator = db.query(Creator).filter(Creator.id == creator_id).first()

    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")

    return creator


@router.put("/{creator_id}", response_model=CreatorOut)
def update_creator(
    creator_id: int,
    creator_data: CreatorUpdate,
    db: Session = Depends(get_db),
):
    creator = db.query(Creator).filter(Creator.id == creator_id).first()

    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")

    update_data = creator_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(creator, key, value)

    db.commit()
    db.refresh(creator)

    return creator


@router.delete("/{creator_id}")
def delete_creator(creator_id: int, db: Session = Depends(get_db)):
    creator = db.query(Creator).filter(Creator.id == creator_id).first()

    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")

    db.delete(creator)
    db.commit()

    return {"message": "Creator deleted successfully"}
