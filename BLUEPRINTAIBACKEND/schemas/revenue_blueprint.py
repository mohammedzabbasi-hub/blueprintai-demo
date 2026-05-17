from typing import List, Optional
from pydantic import BaseModel


class BlueprintStepBase(BaseModel):
    step_number: int
    title: str
    description: str
    action: str
    priority: str = "Medium"
    related_feature: Optional[str] = None
    expected_result: Optional[str] = None
    is_completed: bool = False


class BlueprintStepCreate(BlueprintStepBase):
    pass


class BlueprintStepOut(BlueprintStepBase):
    id: int

    class Config:
        from_attributes = True


class RevenueBlueprintBase(BaseModel):
    shop_id: int
    title: str = "AI Growth Blueprint"
    main_goal: Optional[str] = None
    diagnosis: Optional[str] = None
    summary: Optional[str] = None
    estimated_impact: Optional[str] = None


class RevenueBlueprintCreate(RevenueBlueprintBase):
    steps: List[BlueprintStepCreate]


class RevenueBlueprintOut(RevenueBlueprintBase):
    id: int
    steps: List[BlueprintStepOut] = []

    class Config:
        from_attributes = True


class GenerateBlueprintRequest(BaseModel):
    shop_id: int


class CompleteStepRequest(BaseModel):
    step_id: int
    is_completed: bool = True
