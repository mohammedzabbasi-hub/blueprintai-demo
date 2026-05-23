from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import inspect, text
from db.database import engine
from passlib.hash import pbkdf2_sha256

router = APIRouter(prefix="/auth", tags=["app-login"])

DEMO_ACCOUNTS = {
    "beauty@demo.com": {"password": "demo123", "name": "GlowLab Beauty Team", "shop_ids": [1]},
    "fitness@demo.com": {"password": "demo123", "name": "FitPulse Gear Team", "shop_ids": [2]},
    "home@demo.com": {"password": "demo123", "name": "HomeEase Finds Team", "shop_ids": [3]},
    "agency@demo.com": {"password": "demo123", "name": "BlueprintAI Agency Demo", "shop_ids": [1, 2, 3, 4, 5]},
}

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

def table_exists(table_name):
    return table_name in inspect(engine).get_table_names()

def get_value(row, *keys):
    for key in keys:
        if key in row and row[key] is not None:
            return row[key]
    return None

@router.post("/app-login")
def app_login(payload: LoginRequest):
    email = payload.email.lower().strip()

    if email in DEMO_ACCOUNTS:
        demo = DEMO_ACCOUNTS[email]

        if payload.password != demo["password"]:
            raise HTTPException(status_code=401, detail="Invalid email or password.")

        shop_id = demo["shop_ids"][0]

        return {
            "success": True,
            "token": f"demo-token-{email}",
            "user": {
                "id": email,
                "name": demo["name"],
                "email": email,
                "shop_id": shop_id,
                "shop_ids": demo["shop_ids"],
                "is_demo": True,
            },
            "shop": {
                "id": shop_id,
                "shop_id": shop_id,
                "shop_name": demo["name"],
                "name": demo["name"],
                "is_demo": True,
            },
        }

    if not table_exists("users"):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    with engine.begin() as conn:
        user = conn.execute(
            text("SELECT * FROM users WHERE lower(email) = :email LIMIT 1"),
            {"email": email},
        ).mappings().first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password.")

        stored_hash = get_value(user, "hashed_password", "password_hash")
        plain_password = get_value(user, "password")

        password_ok = False

        if stored_hash:
            try:
                password_ok = pbkdf2_sha256.verify(payload.password, stored_hash)
            except Exception:
                password_ok = False

        if plain_password and payload.password == plain_password:
            password_ok = True

        if not password_ok:
            raise HTTPException(status_code=401, detail="Invalid email or password.")

        user_id = user["id"]
        user_name = get_value(user, "name", "full_name", "team_name", "username") or email

        shop_rows = []
        if table_exists("shops"):
            shop_rows = conn.execute(
                text("SELECT * FROM shops WHERE user_id = :user_id ORDER BY id ASC"),
                {"user_id": user_id},
            ).mappings().all()

        shop_ids = [row["id"] for row in shop_rows]

        if shop_rows:
            first_shop = shop_rows[0]
            shop_name = get_value(first_shop, "shop_name", "name") or "My TikTok Shop"
            shop = {
                "id": first_shop["id"],
                "shop_id": first_shop["id"],
                "shop_name": shop_name,
                "name": shop_name,
                "is_demo": False,
            }
        else:
            shop = {
                "id": None,
                "shop_id": None,
                "shop_name": "My TikTok Shop",
                "name": "My TikTok Shop",
                "is_demo": False,
            }

    return {
        "success": True,
        "token": f"user-token-{user_id}",
        "user": {
            "id": user_id,
            "name": user_name,
            "email": email,
            "shop_id": shop["id"],
            "shop_ids": shop_ids,
            "shop_name": shop["shop_name"],
            "is_demo": False,
        },
        "shop": shop,
    }
