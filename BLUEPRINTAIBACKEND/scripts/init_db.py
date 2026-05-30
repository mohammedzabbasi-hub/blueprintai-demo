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

print("Database tables created/verified.")
