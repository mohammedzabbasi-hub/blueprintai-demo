from db.session import Base, engine

# Import models so SQLAlchemy registers them before create_all()
from models.user import User
from models.shop import Shop
from models.shop_connection import ShopConnection
from models.product import Product
from models.order import Order
from models.creative import Creative
from models.metric import Metric
from models.brief import Brief
from models.recommendation import Recommendation
from models.webhook_event import WebhookEvent
from models.sync_job import SyncJob
from models.video_analysis import VideoAnalysis


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
