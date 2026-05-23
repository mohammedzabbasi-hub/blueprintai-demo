from sqlalchemy import text, inspect
from db.database import engine


def table_exists(table):
    return table in inspect(engine).get_table_names()


def columns(table):
    if not table_exists(table):
        return set()
    return {c["name"] for c in inspect(engine).get_columns(table)}


def add_column(conn, table, col_def):
    name = col_def.split()[0]
    if name not in columns(table):
        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col_def}"))


with engine.begin() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shop_id INTEGER,
        product_name VARCHAR,
        product_id VARCHAR,
        sku VARCHAR,
        category VARCHAR,
        price FLOAT,
        inventory INTEGER,
        image_url TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shop_id INTEGER,
        order_id VARCHAR,
        product_id VARCHAR,
        product_name VARCHAR,
        quantity INTEGER,
        revenue FLOAT,
        buyer_region VARCHAR,
        order_status VARCHAR,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS creators (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shop_id INTEGER,
        name VARCHAR,
        tiktok_handle VARCHAR,
        category VARCHAR,
        follower_count INTEGER,
        total_views INTEGER,
        total_likes INTEGER,
        total_orders INTEGER,
        total_revenue FLOAT,
        notes TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS creatives (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shop_id INTEGER,
        product_id VARCHAR,
        product VARCHAR,
        title VARCHAR,
        creator VARCHAR,
        video_url TEXT,
        thumbnail TEXT,
        insight TEXT,
        transcript TEXT,
        transcript_summary TEXT,
        hook_type VARCHAR,
        creator_type VARCHAR,
        humor_style VARCHAR,
        delivery_style VARCHAR,
        score FLOAT,
        views INTEGER,
        likes INTEGER,
        shares INTEGER,
        clicks INTEGER,
        orders INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """))

    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shop_id INTEGER,
        creative_id INTEGER,
        product_id VARCHAR,
        views INTEGER,
        clicks INTEGER,
        likes INTEGER,
        shares INTEGER,
        orders INTEGER,
        revenue FLOAT,
        ctr FLOAT,
        cvr FLOAT,
        roas FLOAT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """))

    for table in ["products", "orders", "creators", "creatives", "metrics"]:
        add_column(conn, table, "shop_id INTEGER")

print("Core data tables created/verified.")
