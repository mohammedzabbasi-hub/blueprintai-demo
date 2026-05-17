from pydantic import BaseModel, Field


class TotalsOut(BaseModel):
    creatives: int = 0
    briefs: int = 0
    recommendations: int = 0
    analyses: int = 0
    views: int = 0
    clicks: int = 0
    orders: int = 0


class PatternBreakdownOut(BaseModel):
    hooks: dict[str, int] = Field(default_factory=dict)
    creator_types: dict[str, int] = Field(default_factory=dict)
    humor_styles: dict[str, int] = Field(default_factory=dict)
    delivery_styles: dict[str, int] = Field(default_factory=dict)


class CreativeLeaderboardItemOut(BaseModel):
    creative_id: int
    title: str
    product: str
    hook_type: str | None = None
    creator_type: str | None = None
    engagement_score: float = 0.0
    conversion_score: float = 0.0


class DashboardAnalyticsOut(BaseModel):
    totals: TotalsOut
    patterns: PatternBreakdownOut
    leaderboard: list[CreativeLeaderboardItemOut] = Field(default_factory=list)
