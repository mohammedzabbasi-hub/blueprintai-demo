from fastapi import FastAPI
from api.routes import onboarding
from fastapi.middleware.cors import CORSMiddleware

from routes.video_analysis import router as video_analysis_router
from routes.activity_log import router as activity_log_router
from routes.creators import router as creators_router
from routes.demo import router as demo_router
from routes.recommendations import router as recommendations_router

from db.database import Base, engine

# Import all SQLAlchemy models so relationships can resolve correctly
from models.user import User
from models.shop import Shop
from models.creator import Creator
from models.creative import Creative
from models.metric import Metric
from models.product import Product
from models.recommendation import Recommendation
from models.brief import Brief
from models.sync_job import SyncJob
from models.shop_connection import ShopConnection

try:
    from models.video_analysis import VideoAnalysis
except Exception:
    pass

from api.routes.analytics import router as analytics_router
from api.routes.engine import router as engine_router
from api.routes.creatives import router as creatives_router

from app.routes.google_auth import router as google_auth_router
from api.routes.auth import router as auth_router

app = FastAPI()

app.include_router(onboarding.router)
@app.get("/")
def root():
    return {"message": "BluePrintAI backend running"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

import models.revenue_blueprint
Base.metadata.create_all(bind=engine)

app.include_router(analytics_router)
app.include_router(engine_router)
app.include_router(creatives_router, prefix="/creatives", tags=["creatives"])
app.include_router(video_analysis_router)
app.include_router(creators_router)
app.include_router(demo_router)
app.include_router(recommendations_router)

# google_auth.py already has prefix="/auth", so do NOT add another prefix here
app.include_router(google_auth_router)
app.include_router(auth_router, prefix="/auth", tags=["auth"])

from api.routes import briefs

app.include_router(briefs.router, prefix="/briefs", tags=["briefs"])

from routes import revenue_blueprint

app.include_router(revenue_blueprint.router, prefix="/blueprint", tags=["Revenue Blueprint"])

app.include_router(activity_log_router)
