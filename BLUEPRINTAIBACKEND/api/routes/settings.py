from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from deps import get_current_active_user, get_db
from models.user import User
from schemas.settings import SettingsUpdate, UserSettingsOut

router = APIRouter()


@router.get("/me", response_model=UserSettingsOut)
def get_my_settings(
    current_user: User = Depends(get_current_active_user),
):
    return current_user


@router.put("/me", response_model=UserSettingsOut)
def update_my_settings(
    settings_in: SettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if settings_in.name is not None:
        current_user.name = settings_in.name

    if settings_in.email is not None:
        existing_user = (
            db.query(User)
            .filter(User.email == settings_in.email, User.id != current_user.id)
            .first()
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use",
            )
        current_user.email = settings_in.email

    db.commit()
    db.refresh(current_user)
    return current_user
