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


def safe_int(value, default=0):
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def safe_float(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


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
        row.setdefault("order_status", row.get("status") or "imported")
        row.setdefault("raw_payload", json.dumps(row, default=str))
        row.setdefault("created_at", datetime.utcnow().isoformat())

    if table == "creators":
        row.setdefault("handle", row.get("tiktok_handle"))
        row.setdefault("name", row.get("handle") or row.get("tiktok_handle"))

    if table == "creatives":
        row.setdefault("name", row.get("title"))
        row.setdefault("title", row.get("name") or "Imported Creative")
        row.setdefault("thumbnail", row.get("thumbnail_url") or row.get("thumbnail"))
        row.setdefault("promoter_handle", row.get("tiktok_handle") or row.get("handle"))

    return row


def fallback_value(table, col, row, shop_id):
    now = datetime.utcnow().isoformat()
    col_lower = col.lower()

    if col == "shop_id":
        return shop_id
    if table == "creators" and col == "brand_id":
        return shop_id
    if table == "metrics" and col == "creative_id":
        return row.get("creative_id")
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


def resolve_metric_creative_id(conn, row, shop_id):
    if row.get("creative_id"):
        return row.get("creative_id")

    if not table_exists("creatives"):
        return None

    creative_cols = column_info("creatives")
    if "shop_id" not in creative_cols:
        return None

    title = row.get("title") or row.get("creative_title") or row.get("name")
    product = row.get("product") or row.get("product_name")
    creator = row.get("creator") or row.get("tiktok_handle") or row.get("handle")

    if title and "title" in creative_cols:
        found = conn.execute(
            text("""
                SELECT id FROM creatives
                WHERE shop_id = :shop_id AND lower(title) = lower(:title)
                ORDER BY id DESC
                LIMIT 1
            """),
            {"shop_id": shop_id, "title": title},
        ).scalar()
        if found:
            return found

    if product and "product" in creative_cols:
        found = conn.execute(
            text("""
                SELECT id FROM creatives
                WHERE shop_id = :shop_id AND lower(product) = lower(:product)
                ORDER BY id DESC
                LIMIT 1
            """),
            {"shop_id": shop_id, "product": product},
        ).scalar()
        if found:
            return found

    if creator and "creator" in creative_cols:
        found = conn.execute(
            text("""
                SELECT id FROM creatives
                WHERE shop_id = :shop_id AND lower(creator) = lower(:creator)
                ORDER BY id DESC
                LIMIT 1
            """),
            {"shop_id": shop_id, "creator": creator},
        ).scalar()
        if found:
            return found

    return conn.execute(
        text("SELECT id FROM creatives WHERE shop_id = :shop_id ORDER BY id DESC LIMIT 1"),
        {"shop_id": shop_id},
    ).scalar()


def find_duplicate(conn, table, row, shop_id):
    if table == "products" and row.get("name"):
        return conn.execute(
            text("""
                SELECT id FROM products
                WHERE shop_id = :shop_id AND lower(name) = lower(:name)
                LIMIT 1
            """),
            {"shop_id": shop_id, "name": row["name"]},
        ).scalar()

    if table == "creators":
        handle = row.get("tiktok_handle") or row.get("handle")
        name = row.get("name")
        if handle:
            return conn.execute(
                text("""
                    SELECT id FROM creators
                    WHERE brand_id = :shop_id AND lower(tiktok_handle) = lower(:handle)
                    LIMIT 1
                """),
                {"shop_id": shop_id, "handle": handle},
            ).scalar()
        if name:
            return conn.execute(
                text("""
                    SELECT id FROM creators
                    WHERE brand_id = :shop_id AND lower(name) = lower(:name)
                    LIMIT 1
                """),
                {"shop_id": shop_id, "name": name},
            ).scalar()

    if table == "creatives" and row.get("title"):
        return conn.execute(
            text("""
                SELECT id FROM creatives
                WHERE shop_id = :shop_id AND lower(title) = lower(:title)
                LIMIT 1
            """),
            {"shop_id": shop_id, "title": row["title"]},
        ).scalar()

    if table == "orders":
        order_id = row.get("tiktok_order_id") or row.get("order_id")
        if order_id:
            return conn.execute(
                text("SELECT id FROM orders WHERE tiktok_order_id = :order_id LIMIT 1"),
                {"order_id": order_id},
            ).scalar()

    if table == "metrics" and row.get("creative_id"):
        return conn.execute(
            text("""
                SELECT id FROM metrics
                WHERE creative_id = :creative_id
                  AND COALESCE(views, 0) = :views
                  AND COALESCE(clicks, 0) = :clicks
                  AND COALESCE(orders, 0) = :orders
                  AND COALESCE(likes, 0) = :likes
                  AND COALESCE(shares, 0) = :shares
                LIMIT 1
            """),
            {
                "creative_id": row["creative_id"],
                "views": int(row.get("views") or 0),
                "clicks": int(row.get("clicks") or 0),
                "orders": int(row.get("orders") or 0),
                "likes": int(row.get("likes") or 0),
                "shares": int(row.get("shares") or 0),
            },
        ).scalar()

    return None


def calculate_metric_rates(row):
    views = safe_float(row.get("views"))
    clicks = safe_float(row.get("clicks"))
    orders = safe_float(row.get("orders"))
    revenue = safe_float(row.get("revenue") or row.get("total_revenue"))
    row.setdefault("ctr", round(clicks / views, 4) if views else 0)
    row.setdefault("cvr", round(orders / clicks, 4) if clicks else 0)
    if "roas" not in row and revenue:
        # The current metrics schema has no ad_spend/revenue columns, so keep any
        # imported ROAS if present and otherwise leave ROAS neutral.
        row["roas"] = row.get("roas") or 0
    return row


def sync_creative_from_metric(conn, row):
    creative_id = row.get("creative_id")
    if not creative_id or not table_exists("creatives"):
        return

    cols = column_info("creatives")
    updates = {}
    for field in ["views", "likes", "shares", "clicks", "orders"]:
        if field in cols and field in row:
            updates[field] = safe_int(row.get(field))

    if "comments" in cols and "comments" in row:
        updates["comments"] = safe_int(row.get("comments"))

    views = safe_float(row.get("views"))
    likes = safe_float(row.get("likes"))
    shares = safe_float(row.get("shares"))
    clicks = safe_float(row.get("clicks"))
    orders = safe_float(row.get("orders"))

    if "engagement_score" in cols and views:
        updates["engagement_score"] = round(((likes + shares) / views) * 100, 2)
    if "conversion_score" in cols and views:
        updates["conversion_score"] = round(((clicks + orders * 4) / views) * 100, 2)
    if "score" in cols and views:
        ctr = clicks / views if views else 0
        cvr = orders / clicks if clicks else 0
        updates["score"] = min(100, round((ctr * 1000) + (cvr * 250) + 40))

    if not updates:
        return

    set_sql = ", ".join([f"{key} = :{key}" for key in updates])
    updates["creative_id"] = creative_id
    conn.execute(
        text(f"UPDATE creatives SET {set_sql} WHERE id = :creative_id"),
        updates,
    )


def sync_creator_from_creative(conn, creative_id):
    if not creative_id or not table_exists("creators") or not table_exists("creatives"):
        return

    creator_cols = column_info("creators")
    creative = conn.execute(
        text("""
            SELECT shop_id, creator, promoter_handle, views, likes, comments, shares, orders
            FROM creatives
            WHERE id = :creative_id
            LIMIT 1
        """),
        {"creative_id": creative_id},
    ).mappings().first()

    if not creative:
        return

    creator_name = creative.get("creator")
    handle = creative.get("promoter_handle") or creator_name
    if not creator_name and not handle:
        return

    creator_id = None
    if handle and "tiktok_handle" in creator_cols:
        creator_id = conn.execute(
            text("""
                SELECT id FROM creators
                WHERE brand_id = :shop_id AND lower(tiktok_handle) = lower(:handle)
                LIMIT 1
            """),
            {"shop_id": creative["shop_id"], "handle": handle},
        ).scalar()

    if not creator_id and creator_name:
        creator_id = conn.execute(
            text("""
                SELECT id FROM creators
                WHERE brand_id = :shop_id AND lower(name) = lower(:name)
                LIMIT 1
            """),
            {"shop_id": creative["shop_id"], "name": creator_name},
        ).scalar()

    if not creator_id:
        return

    updates = {}
    field_map = {
        "total_videos": 1,
        "total_views": safe_int(creative.get("views")),
        "total_likes": safe_int(creative.get("likes")),
        "total_comments": safe_int(creative.get("comments")),
        "total_shares": safe_int(creative.get("shares")),
        "total_conversions": safe_int(creative.get("orders")),
    }
    for field, value in field_map.items():
        if field in creator_cols:
            updates[field] = value

    revenue = conn.execute(
        text("SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE shop_id = :shop_id"),
        {"shop_id": creative["shop_id"]},
    ).scalar()
    if "total_revenue" in creator_cols:
        updates["total_revenue"] = safe_int(revenue)

    if not updates:
        return

    set_sql = ", ".join([f"{key} = :{key}" for key in updates])
    updates["creator_id"] = creator_id
    conn.execute(
        text(f"UPDATE creators SET {set_sql} WHERE id = :creator_id"),
        updates,
    )


def invalidate_revenue_blueprints(conn, shop_id):
    if not table_exists("revenue_blueprints"):
        return

    blueprint_ids = [
        row[0]
        for row in conn.execute(
            text("SELECT id FROM revenue_blueprints WHERE shop_id = :shop_id"),
            {"shop_id": shop_id},
        ).all()
    ]
    if not blueprint_ids:
        return

    if table_exists("revenue_blueprint_steps"):
        conn.execute(
            text("""
                DELETE FROM revenue_blueprint_steps
                WHERE blueprint_id IN (
                    SELECT id FROM revenue_blueprints WHERE shop_id = :shop_id
                )
            """),
            {"shop_id": shop_id},
        )

    conn.execute(
        text("DELETE FROM revenue_blueprints WHERE shop_id = :shop_id"),
        {"shop_id": shop_id},
    )


def insert_dynamic(conn, table, row, shop_id, return_existing=False):
    cols = column_info(table)
    actual_cols = set(cols.keys())

    row = normalize_row(table, row)
    row["shop_id"] = shop_id

    if table == "creators":
        row["brand_id"] = shop_id

    if table == "metrics":
        row["creative_id"] = resolve_metric_creative_id(conn, row, shop_id)
        if not row["creative_id"]:
            return None
        row = calculate_metric_rates(row)

    duplicate_id = find_duplicate(conn, table, row, shop_id)
    if duplicate_id:
        if table == "metrics":
            sync_creative_from_metric(conn, row)
            sync_creator_from_creative(conn, row.get("creative_id"))
        return duplicate_id if return_existing else None

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
            value = fallback_value(table, col, row, shop_id)
            if value is not None:
                filtered[col] = value

    if not filtered:
        return None

    col_sql = ", ".join(filtered.keys())
    bind_sql = ", ".join([f":{k}" for k in filtered.keys()])

    result = conn.execute(
        text(f"INSERT INTO {table} ({col_sql}) VALUES ({bind_sql})"),
        filtered,
    )

    inserted_id = result.lastrowid

    if table == "metrics":
        sync_creative_from_metric(conn, row)
        sync_creator_from_creative(conn, row.get("creative_id"))

    return inserted_id


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
    try:
        data = json.loads(content.decode("utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid JSON import file: {exc.msg}") from exc

    inserted_totals = {}
    skipped_totals = {}
    imported_creative_ids = []

    with engine.begin() as conn:
        for table_name in ["products", "creators", "creatives", "orders", "metrics"]:
            rows = data.get(table_name, [])

            if not isinstance(rows, list):
                continue

            inserted = 0
            skipped = 0

            for row in rows:
                if isinstance(row, dict):
                    working_row = normalize_row(table_name, row)

                    if table_name == "metrics" and not working_row.get("creative_id"):
                        metric_index = inserted + skipped
                        if len(imported_creative_ids) == 1:
                            working_row["creative_id"] = imported_creative_ids[0]
                        elif metric_index < len(imported_creative_ids):
                            working_row["creative_id"] = imported_creative_ids[metric_index]

                    if table_name == "metrics":
                        working_row["creative_id"] = resolve_metric_creative_id(conn, working_row, shop_id)
                        working_row = calculate_metric_rates(working_row)

                    duplicate_id = find_duplicate(conn, table_name, working_row, shop_id)
                    inserted_id = insert_dynamic(
                        conn,
                        table_name,
                        working_row,
                        shop_id,
                        return_existing=True,
                    )

                    if table_name == "creatives" and inserted_id:
                        imported_creative_ids.append(inserted_id)

                    if inserted_id and not duplicate_id:
                        inserted += 1
                    else:
                        skipped += 1

            inserted_totals[table_name] = inserted
            skipped_totals[table_name] = skipped

        if sum(inserted_totals.values()) > 0:
            invalidate_revenue_blueprints(conn, shop_id)

    return {
        "success": True,
        "shop_id": shop_id,
        "inserted": inserted_totals,
        "skipped_duplicates": skipped_totals,
        "inserted_total": sum(inserted_totals.values()),
        "skipped_total": sum(skipped_totals.values()),
    }


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
            if table_name == "creators" and table_exists(table_name) and {"shop_id", "brand_id"} <= set(cols):
                count = conn.execute(
                    text("""
                        SELECT COUNT(*) FROM creators
                        WHERE shop_id = :shop_id OR brand_id = :shop_id
                    """),
                    {"shop_id": shop_id},
                ).scalar() or 0
            elif table_exists(table_name) and "shop_id" in cols:
                count = conn.execute(
                    text(f"SELECT COUNT(*) FROM {table_name} WHERE shop_id = :shop_id"),
                    {"shop_id": shop_id},
                ).scalar() or 0
            elif table_name == "creators" and table_exists(table_name) and "brand_id" in cols:
                count = conn.execute(
                    text("SELECT COUNT(*) FROM creators WHERE brand_id = :shop_id"),
                    {"shop_id": shop_id},
                ).scalar() or 0
            elif table_name == "metrics" and table_exists("metrics") and table_exists("creatives"):
                count = conn.execute(
                    text("""
                        SELECT COUNT(metrics.id)
                        FROM metrics
                        JOIN creatives ON creatives.id = metrics.creative_id
                        WHERE creatives.shop_id = :shop_id
                    """),
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
            if table_name == "creators" and table_exists(table_name) and {"shop_id", "brand_id"} <= set(cols):
                result = conn.execute(
                    text("""
                        DELETE FROM creators
                        WHERE shop_id = :shop_id OR brand_id = :shop_id
                    """),
                    {"shop_id": shop_id},
                )
                deleted[table_name] = result.rowcount
            elif table_exists(table_name) and "shop_id" in cols:
                result = conn.execute(
                    text(f"DELETE FROM {table_name} WHERE shop_id = :shop_id"),
                    {"shop_id": shop_id},
                )
                deleted[table_name] = result.rowcount
            elif table_name == "creators" and table_exists(table_name) and "brand_id" in cols:
                result = conn.execute(
                    text("DELETE FROM creators WHERE brand_id = :shop_id"),
                    {"shop_id": shop_id},
                )
                deleted[table_name] = result.rowcount
            elif table_name == "metrics" and table_exists("metrics") and table_exists("creatives"):
                result = conn.execute(
                    text("""
                        DELETE FROM metrics
                        WHERE creative_id IN (
                            SELECT id FROM creatives WHERE shop_id = :shop_id
                        )
                    """),
                    {"shop_id": shop_id},
                )
                deleted[table_name] = result.rowcount

        invalidate_revenue_blueprints(conn, shop_id)

    return {"success": True, "shop_id": shop_id, "deleted": deleted}
