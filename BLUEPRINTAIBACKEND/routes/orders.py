from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db.database import get_db
from models.order import Order
from schemas.order import OrderOut, OrderListResponse
from services.tiktok_order_service import sync_orders_for_shop

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=OrderListResponse)
def list_orders(
    shop_id: int = Query(...),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    items = (
        db.query(Order)
        .filter(Order.shop_id == shop_id)
        .order_by(Order.created_at.desc())
        .limit(limit)
        .all()
    )
    return OrderListResponse(items=items, count=len(items))


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    item = db.query(Order).filter(Order.id == order_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Order not found")
    return item


@router.post("/sync/{shop_id}")
def sync_orders(shop_id: int, db: Session = Depends(get_db)):
    count = sync_orders_for_shop(db=db, shop_id=shop_id)
    return {"success": True, "synced_orders": count}
