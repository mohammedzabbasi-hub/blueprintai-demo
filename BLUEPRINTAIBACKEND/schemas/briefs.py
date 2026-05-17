from pydantic import BaseModel, Field


class BriefGenerateRequest(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=255)
    brand_name: str | None = None


class BriefOut(BaseModel):
    id: int | None = None
    product: str
    brief_title: str | None = None
    hook: str
    creator_type: str
    tone: str | None = None
    cta: str | None = None
    target_audience: str | None = None
    primary_angle: str | None = None
    secondary_angle: str | None = None
    structure: str | None = None
    reasoning: str | None = None
    script: str | None = None
    shot_list: str | None = None
    dos: str | None = None
    donts: str | None = None
    references: str | None = None

    model_config = {"from_attributes": True}
