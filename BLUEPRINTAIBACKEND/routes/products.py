from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db.database import get_db
from models.product import Product
from schemas.product import ProductOut, ProductListResponse
from services.tiktok_product_service import sync_products_for_shop

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=ProductListResponse)
def list_products(
    shop_id: int = Query(...),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    items = (
        db.query(Product)
        .filter(Product.shop_id == shop_id)
        .order_by(Product.updated_at.desc())
        .limit(limit)
        .all()
    )
    return ProductListResponse(items=items, count=len(items))


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    item = db.query(Product).filter(Product.id == product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Product not found")
    return item


@router.post("/sync/{shop_id}")
def sync_products(shop_id: int, db: Session = Depends(get_db)):
    count = sync_products_for_shop(db=db, shop_id=shop_id)
    return {"success": True, "synced_products": count}
