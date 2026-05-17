from pydantic import BaseModel, EmailStr, Field


class SettingsUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None


class UserSettingsOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool

    model_config = {"from_attributes": True}
