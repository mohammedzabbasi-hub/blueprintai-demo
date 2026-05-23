from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import inspect, text
from db.database import engine
from passlib.hash import pbkdf2_sha256

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


class OnboardingCreateRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    store_name: str
    niche: str | None = None
    average_price: float | None = None
    main_goal: str | None = None


def ensure_min_tables(conn):
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email VARCHAR UNIQUE,
        name VARCHAR,
        hashed_password VARCHAR,
        is_active BOOLEAN DEFAULT 1
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS shops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        shop_name VARCHAR,
        name VARCHAR,
        tiktok_shop_id VARCHAR,
        shop_code VARCHAR,
        region VARCHAR DEFAULT 'US',
        currency VARCHAR DEFAULT 'USD',
        category VARCHAR,
        connection_id VARCHAR,
        raw_payload TEXT
    )
    """))


def columns(table_name):
    return {c["name"] for c in inspect(engine).get_columns(table_name)}


def insert_dynamic(conn, table_name, values):
    actual_cols = columns(table_name)
    filtered = {k: v for k, v in values.items() if k in actual_cols and v is not None}

    col_sql = ", ".join(filtered.keys())
    bind_sql = ", ".join([f":{k}" for k in filtered.keys()])

    result = conn.execute(
        text(f"INSERT INTO {table_name} ({col_sql}) VALUES ({bind_sql})"),
        filtered,
    )
    return result.lastrowid


@router.post("/create-account")
def create_onboarding_account(payload: OnboardingCreateRequest):
    if len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")

    email = payload.email.lower().strip()
    hashed = pbkdf2_sha256.hash(payload.password)

    with engine.begin() as conn:
        ensure_min_tables(conn)

        user_cols = columns("users")
        if "email" in user_cols:
            existing = conn.execute(
                text("SELECT id FROM users WHERE lower(email) = :email LIMIT 1"),
                {"email": email},
            ).mappings().first()
            if existing:
                raise HTTPException(status_code=409, detail="An account with this email already exists.")

        user_id = insert_dynamic(conn, "users", {
            "email": email,
            "name": payload.name,
            "full_name": payload.name,
            "team_name": payload.name,
            "username": email,
            "hashed_password": hashed,
            "password_hash": hashed,
            "is_active": True,
            "is_demo": False,
        })

        shop_id = insert_dynamic(conn, "shops", {
            "user_id": user_id,
            "shop_name": payload.store_name,
            "name": payload.store_name,
            "tiktok_shop_id": f"custom_shop_{user_id}",
            "shop_code": f"custom_shop_{user_id}",
            "region": "US",
            "currency": "USD",
            "category": payload.niche,
            "connection_id": f"onboarding_{user_id}",
            "raw_payload": str({
                "niche": payload.niche,
                "average_price": payload.average_price,
                "main_goal": payload.main_goal,
                "source": "onboarding",
            }),
        })

    return {
        "success": True,
        "token": f"demo-onboarding-token-{user_id}",
        "user": {
            "id": user_id,
            "name": payload.name,
            "email": email,
            "shop_id": shop_id,
            "shop_name": payload.store_name,
        },
        "shop": {
            "id": shop_id,
            "shop_id": shop_id,
            "shop_name": payload.store_name,
            "name": payload.store_name,
            "category": payload.niche,
            "average_price": payload.average_price,
            "main_goal": payload.main_goal,
        },
    }
