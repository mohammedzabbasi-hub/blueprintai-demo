import os
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from deps import get_db
from models.user import User
from utils.security import create_access_token

load_dotenv()

router = APIRouter(prefix="/auth", tags=["auth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


class GoogleAuthRequest(BaseModel):
    credential: str


@router.post("/google")
def google_login(payload: GoogleAuthRequest, db: Session = Depends(get_db)):
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Missing GOOGLE_CLIENT_ID")

    try:
        idinfo = id_token.verify_oauth2_token(
            payload.credential,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    email = idinfo.get("email")
    name = idinfo.get("name") or email
    google_sub = idinfo.get("sub")
    email_verified = idinfo.get("email_verified", False)

    if not email or not google_sub:
        raise HTTPException(status_code=400, detail="Missing Google account data")

    if not email_verified:
        raise HTTPException(status_code=400, detail="Google email is not verified")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            name=name,
            email=email,
            hashed_password="google_oauth_user",
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(subject=user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }
