from typing import Any
from pydantic import BaseModel, Field, HttpUrl


class VideoIngestRequest(BaseModel):
    url: HttpUrl | None = None
    brand_name: str | None = None
    product_name: str | None = None
    competitor_brand_names: list[str] = Field(default_factory=list)


class VideoSignalOut(BaseModel):
    hook_type: str | None = None
    hook_text: str | None = None
    humor_style: str | None = None
    delivery_style: str | None = None
    creator_style: str | None = None
    promoter_type: str | None = None
    subject_focus: str | None = None
    pacing: str | None = None
    cta_style: str | None = None


class VideoAnalysisOut(BaseModel):
    transcript: str | None = None
    transcript_summary: str | None = None
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    performance_hypothesis: str | None = None
    signals: VideoSignalOut
    raw: dict[str, Any] = Field(default_factory=dict)


class CompareVideosRequest(BaseModel):
    creative_ids: list[int] = Field(default_factory=list)
    brand_names: list[str] = Field(default_factory=list)
    product_name: str | None = None


class ComparisonInsightOut(BaseModel):
    best_hooks: list[str] = Field(default_factory=list)
    best_creator_types: list[str] = Field(default_factory=list)
    best_humor_styles: list[str] = Field(default_factory=list)
    best_delivery_styles: list[str] = Field(default_factory=list)
    best_promoter_types: list[str] = Field(default_factory=list)
    patterns: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
