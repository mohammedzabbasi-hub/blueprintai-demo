from enum import Enum


class PlatformEnum(str, Enum):
    TIKTOK = "tiktok"


class SyncJobTypeEnum(str, Enum):
    FULL_SYNC = "full_sync"
    PRODUCTS_SYNC = "products_sync"
    ORDERS_SYNC = "orders_sync"
    CREATIVES_SYNC = "creatives_sync"
    AI_ANALYSIS = "ai_analysis"
    RECOMMENDATIONS_REFRESH = "recommendations_refresh"
    BRIEF_GENERATION = "brief_generation"


class SyncJobStatusEnum(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class RecommendationCategoryEnum(str, Enum):
    USE_MORE = "useMore"
    NEXT_TEST = "nextTest"
    AVOID = "avoid"


class PriorityEnum(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    
