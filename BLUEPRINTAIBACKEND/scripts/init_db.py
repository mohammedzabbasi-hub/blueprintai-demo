from db.database import Base, engine

import models.user
import models.shop
import models.shop_connection
import models.creative
import models.creator
import models.metric
import models.product
import models.order
import models.recommendation
import models.brief
import models.revenue_blueprint
import models.video_analysis
import models.activity_log

print("Registered SQLAlchemy tables:", sorted(Base.metadata.tables.keys()))
Base.metadata.create_all(bind=engine)

with engine.begin() as conn:
    conn.exec_driver_sql("""
    CREATE TABLE IF NOT EXISTS revenue_blueprints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shop_id INTEGER NOT NULL,
        title VARCHAR,
        main_goal VARCHAR,
        diagnosis TEXT,
        summary TEXT,
        estimated_impact TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.exec_driver_sql("""
    CREATE TABLE IF NOT EXISTS blueprint_steps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        blueprint_id INTEGER,
        step_number INTEGER,
        title VARCHAR,
        description TEXT,
        category VARCHAR,
        completed BOOLEAN DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(blueprint_id) REFERENCES revenue_blueprints(id)
    )
    """)

print("Database tables created/verified.")
