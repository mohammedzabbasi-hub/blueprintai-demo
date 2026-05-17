from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from deps import get_db
from schemas.briefs import BriefGenerateRequest, BriefOut
from services.brief_service import generate_brief

router = APIRouter()


@router.post("/generate", response_model=BriefOut, status_code=status.HTTP_200_OK)
def generate_ad_brief(
    brief_in: BriefGenerateRequest,
    db: Session = Depends(get_db),
):
    brief = generate_brief(
        db=db,
        shop_id=1,
        product_name=brief_in.product_name,
        brand_name=brief_in.brand_name,
    )

    return brief
