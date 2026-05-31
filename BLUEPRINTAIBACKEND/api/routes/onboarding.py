from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from db.database import get_db
from deps import get_current_active_user

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


class OnboardingSave(BaseModel):
    store_name: str | None = None
    niche: str | None = None
    average_price: str | None = None
    main_goal: str | None = None
    connected_shop_id: int | None = None
    completed: bool = False


def ensure_table(db: Session):
    dialect_name = db.get_bind().dialect.name

    if dialect_name == "sqlite":
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS user_onboarding (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                store_name TEXT,
                niche TEXT,
                average_price TEXT,
                main_goal TEXT,
                connected_shop_id INTEGER,
                completed INTEGER DEFAULT 0
            )
        """))
    else:
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS user_onboarding (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL UNIQUE,
                store_name TEXT,
                niche TEXT,
                average_price TEXT,
                main_goal TEXT,
                connected_shop_id INTEGER,
                completed BOOLEAN DEFAULT FALSE
            )
        """))

    db.commit()


def serialize_completed(value: bool, db: Session):
    if db.get_bind().dialect.name == "sqlite":
        return 1 if value else 0
    return bool(value)


@router.get("/me")
def get_my_onboarding(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    ensure_table(db)

    row = db.execute(
        text("SELECT * FROM user_onboarding WHERE user_id = :user_id"),
        {"user_id": current_user.id},
    ).mappings().first()

    if not row:
        return {
            "store_name": "",
            "niche": "",
            "average_price": "",
            "main_goal": "",
            "connected_shop_id": None,
            "completed": False,
        }

    return {
        "store_name": row["store_name"] or "",
        "niche": row["niche"] or "",
        "average_price": row["average_price"] or "",
        "main_goal": row["main_goal"] or "",
        "connected_shop_id": row["connected_shop_id"],
        "completed": bool(row["completed"]),
    }


@router.post("/me")
def save_my_onboarding(
    payload: OnboardingSave,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    ensure_table(db)

    db.execute(
        text("""
            INSERT INTO user_onboarding (
                user_id, store_name, niche, average_price, main_goal, connected_shop_id, completed
            )
            VALUES (
                :user_id, :store_name, :niche, :average_price, :main_goal, :connected_shop_id, :completed
            )
            ON CONFLICT(user_id) DO UPDATE SET
                store_name = excluded.store_name,
                niche = excluded.niche,
                average_price = excluded.average_price,
                main_goal = excluded.main_goal,
                connected_shop_id = excluded.connected_shop_id,
                completed = excluded.completed
        """),
        {
            "user_id": current_user.id,
            "store_name": payload.store_name,
            "niche": payload.niche,
            "average_price": payload.average_price,
            "main_goal": payload.main_goal,
            "connected_shop_id": payload.connected_shop_id,
            "completed": serialize_completed(payload.completed, db),
        },
    )

    db.commit()

    return {"success": True, "message": "Onboarding saved"}
