from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from deps import get_db
from schemas.revenue_blueprint import (
    GenerateBlueprintRequest,
    RevenueBlueprintOut,
    CompleteStepRequest,
    BlueprintStepOut,
)
from services.blueprint_engine import (
    create_blueprint,
    get_latest_blueprint,
    update_step_completion,
)

router = APIRouter()


@router.post("/generate", response_model=RevenueBlueprintOut)
def generate_blueprint(request: GenerateBlueprintRequest, db: Session = Depends(get_db)):
    blueprint = create_blueprint(db, request.shop_id)

    if not blueprint:
        raise HTTPException(status_code=500, detail="Failed to generate blueprint.")

    return blueprint


@router.get("/{shop_id}/latest", response_model=RevenueBlueprintOut)
def latest_blueprint(shop_id: int, db: Session = Depends(get_db)):
    blueprint = get_latest_blueprint(db, shop_id)

    if not blueprint:
        blueprint = create_blueprint(db, shop_id)

    return blueprint


@router.post("/complete-step", response_model=BlueprintStepOut)
def complete_blueprint_step(request: CompleteStepRequest, db: Session = Depends(get_db)):
    step = update_step_completion(db, request.step_id, request.is_completed)

    if not step:
        raise HTTPException(status_code=404, detail="Blueprint step not found.")

    return step
