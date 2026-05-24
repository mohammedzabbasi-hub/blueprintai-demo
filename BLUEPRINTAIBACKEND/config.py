from pathlib import Path

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent
PLACEHOLDER_SECRET_KEYS = {
    "",
    "change-me",
    "change-me-super-secret",
    "replace-with-a-long-random-secret",
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "BlueprintAI API"
    APP_ENV: str = "development"
    DEBUG: bool = True

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    SECRET_KEY: str = "change-me-super-secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str = "sqlite:///./blueprintai.db"

    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:8080,http://127.0.0.1:8080"

    TIKTOK_CLIENT_ID: str = ""
    TIKTOK_CLIENT_SECRET: str = ""
    TIKTOK_REDIRECT_URI: str = ""
    TIKTOK_API_BASE_URL: str = "https://open-api.tiktokglobalshop.com"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-5.4"

    MEDIA_ROOT: str = str(BASE_DIR / "storage")
    RAW_VIDEO_DIR: str = str(BASE_DIR / "storage" / "raw_videos")
    FRAME_DIR: str = str(BASE_DIR / "storage" / "frames")
    AUDIO_DIR: str = str(BASE_DIR / "storage" / "audio")
    TRANSCRIPT_DIR: str = str(BASE_DIR / "storage" / "transcripts")
    THUMBNAIL_DIR: str = str(BASE_DIR / "storage" / "thumbnails")
    TEMP_DIR: str = str(BASE_DIR / "storage" / "temp")

    FRAME_SAMPLE_SECONDS: int = 2
    ANALYSIS_MAX_FRAMES: int = 10

    @field_validator("APP_ENV", mode="before")
    @classmethod
    def normalize_app_env(cls, value):
        return str(value or "development").strip().lower()

    @model_validator(mode="after")
    def validate_production_secret_key(self):
        secret_key = str(self.SECRET_KEY or "").strip()

        if self.APP_ENV == "production" and secret_key in PLACEHOLDER_SECRET_KEYS:
            raise ValueError(
                "SECRET_KEY must be set to a strong non-placeholder value when APP_ENV=production"
            )

        self.SECRET_KEY = secret_key
        return self

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()


def ensure_storage_dirs() -> None:
    for path in [
        settings.MEDIA_ROOT,
        settings.RAW_VIDEO_DIR,
        settings.FRAME_DIR,
        settings.AUDIO_DIR,
        settings.TRANSCRIPT_DIR,
        settings.THUMBNAIL_DIR,
        settings.TEMP_DIR,
    ]:
        Path(path).mkdir(parents=True, exist_ok=True)
