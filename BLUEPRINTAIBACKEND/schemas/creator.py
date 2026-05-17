from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CreatorBase(BaseModel):
    name: str
    tiktok_handle: str
    profile_image: Optional[str] = None
    follower_count: int = 0
    category: Optional[str] = None
    notes: Optional[str] = None

    total_videos: int = 0
    total_views: int = 0
    total_likes: int = 0
    total_comments: int = 0
    total_shares: int = 0
    total_conversions: int = 0
    total_revenue: int = 0


class CreatorCreate(CreatorBase):
    user_id: Optional[int] = None
    brand_id: Optional[int] = None


class CreatorUpdate(BaseModel):
    name: Optional[str] = None
    tiktok_handle: Optional[str] = None
    profile_image: Optional[str] = None
    follower_count: Optional[int] = None
    category: Optional[str] = None
    notes: Optional[str] = None

    total_videos: Optional[int] = None
    total_views: Optional[int] = None
    total_likes: Optional[int] = None
    total_comments: Optional[int] = None
    total_shares: Optional[int] = None
    total_conversions: Optional[int] = None
    total_revenue: Optional[int] = None


class CreatorOut(CreatorBase):
    id: int
    user_id: Optional[int] = None
    brand_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
