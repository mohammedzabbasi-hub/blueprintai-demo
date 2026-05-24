from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy import text, inspect
from db.database import engine
from deps import get_current_active_user
from models.user import User
from routes.login import DEMO_ACCOUNTS
from datetime import datetime
import csv
import io
import json

router = APIRouter(prefix="/data-import", tags=["data-import"])

ALLOWED_TABLES = {"products", "orders", "creators", "creatives", "metrics"}


def table_exists(table):
    return table in inspect(engine).get_table_names()


def column_info(table):
    if not table_exists(table):
        return {}
    return {c["name"]: c for c in inspect(engine).get_columns(table)}


def verify_shop_owner(shop_id: int, current_user: User):
    if not table_exists("shops"):
        raise HTTPException(status_code=404, detail="Shop not found.")

    with engine.begin() as conn:
        shop = conn.execute(
            text("SELECT id, user_id, tiktok_shop_id FROM shops WHERE id = :shop_id LIMIT 1"),
            {"shop_id": shop_id},
        ).mappings().first()

    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found.")

    email = str(getattr(current_user, "email", "") or "").lower()
    demo_account = DEMO_ACCOUNTS.get(email)
    is_allowed_demo_shop = (
        demo_account is not None
        and shop_id in demo_account["shop_ids"]
        and str(shop.get("tiktok_shop_id") or "").startswith("demo_shop_")
    )

    if is_allowed_demo_shop:
        return shop

    if shop["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have access to this shop.")

    return shop


def clean_value(value):
    if value == "":
        return None
    return value


def normalize_row(table, row):
    row = {str(k).strip(): clean_value(v) for k, v in row.items()}

    if table == "products":
        row.setdefault("name", row.get("product_name") or row.get("title"))
        row.setdefault("title", row.get("product_name") or row.get("name"))

    if table == "orders":
        row.setdefault("tiktok_order_id", row.get("order_id"))
        row.setdefault("order_id", row.get("tiktok_order_id"))
        row.setdefault("total_amount", row.get("revenue"))
        row.setdefault("status", row.get("order_status"))
        row.setdefault("created_at", datetime.utcnow().isoformat())

    if table == "creators":
        row.setdefault("handle", row.get("tiktok_handle"))
        row.setdefault("name", row.get("handle") or row.get("tiktok_handle"))

    if table == "creatives":
        row.setdefault("name", row.get("title"))
        row.setdefault("title", row.get("name") or "Imported Creative")

    return row


def fallback_value(table, col, row, shop_id):
    now = datetime.utcnow().isoformat()
    col_lower = col.lower()

    if col == "shop_id":
        return shop_id
    if col_lower in ["created_at", "updated_at", "date", "order_date"]:
        return now
    if col_lower in ["name", "title", "product_name"]:
        return row.get("product_name") or row.get("title") or row.get("name") or "Imported Item"
    if col_lower in ["creator", "handle", "tiktok_handle"]:
        return row.get("creator") or row.get("handle") or row.get("tiktok_handle") or "Imported Creator"
    if col_lower in ["order_id", "tiktok_order_id"]:
        return row.get("order_id") or row.get("tiktok_order_id") or f"imported_order_{shop_id}_{int(datetime.utcnow().timestamp())}"
    if col_lower in ["status", "order_status"]:
        return row.get("order_status") or "imported"
    if col_lower in ["category", "niche"]:
        return row.get("category") or "Imported"
    if col_lower in ["currency"]:
        return "USD"

    return 0


def insert_dynamic(conn, table, row, shop_id):
    cols = column_info(table)
    actual_cols = set(cols.keys())

    row = normalize_row(table, row)
    row["shop_id"] = shop_id

    filtered = {
        k: v for k, v in row.items()
        if k in actual_cols and v is not None
    }

    for col, meta in cols.items():
        if meta.get("primary_key"):
            continue

        nullable = meta.get("nullable", True)
        has_default = meta.get("default") is not None

        if not nullable and col not in filtered and not has_default:
            filtered[col] = fallback_value(table, col, row, shop_id)

    if not filtered:
        return None

    col_sql = ", ".join(filtered.keys())
    bind_sql = ", ".join([f":{k}" for k in filtered.keys()])

    result = conn.execute(
        text(f"INSERT INTO {table} ({col_sql}) VALUES ({bind_sql})"),
        filtered,
    )

    return result.lastrowid


@router.post("/csv")
async def import_csv(
    shop_id: int = Form(...),
    table_name: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
):
    verify_shop_owner(shop_id, current_user)

    table_name = table_name.strip().lower()

    if table_name not in ALLOWED_TABLES:
        raise HTTPException(status_code=400, detail="Invalid table name.")

    content = await file.read()
    decoded = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded))

    inserted = 0

    with engine.begin() as conn:
        for row in reader:
            if insert_dynamic(conn, table_name, row, shop_id):
                inserted += 1

    return {"success": True, "shop_id": shop_id, "table": table_name, "inserted": inserted}


@router.post("/json")
async def import_json(
    shop_id: int = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
):
    verify_shop_owner(shop_id, current_user)

    content = await file.read()
    data = json.loads(content.decode("utf-8-sig"))

    totals = {}

    with engine.begin() as conn:
        for table_name in ALLOWED_TABLES:
            rows = data.get(table_name, [])

            if not isinstance(rows, list):
                continue

            count = 0

            for row in rows:
                if isinstance(row, dict):
                    if insert_dynamic(conn, table_name, row, shop_id):
                        count += 1

            totals[table_name] = count

    return {"success": True, "shop_id": shop_id, "inserted": totals}


@router.get("/summary")
def import_summary(
    shop_id: int,
    current_user: User = Depends(get_current_active_user),
):
    verify_shop_owner(shop_id, current_user)

    summary = {}

    with engine.begin() as conn:
        for table_name in ALLOWED_TABLES:
            cols = column_info(table_name)
            if table_exists(table_name) and "shop_id" in cols:
                count = conn.execute(
                    text(f"SELECT COUNT(*) FROM {table_name} WHERE shop_id = :shop_id"),
                    {"shop_id": shop_id},
                ).scalar() or 0
            else:
                count = 0

            summary[table_name] = count

    return {"shop_id": shop_id, "summary": summary}


@router.delete("/clear")
def clear_shop_data(
    shop_id: int,
    current_user: User = Depends(get_current_active_user),
):
    verify_shop_owner(shop_id, current_user)

    deleted = {}

    with engine.begin() as conn:
        for table_name in ALLOWED_TABLES:
            cols = column_info(table_name)
            if table_exists(table_name) and "shop_id" in cols:
                result = conn.execute(
                    text(f"DELETE FROM {table_name} WHERE shop_id = :shop_id"),
                    {"shop_id": shop_id},
                )
                deleted[table_name] = result.rowcount

    return {"success": True, "shop_id": shop_id, "deleted": deleted}
