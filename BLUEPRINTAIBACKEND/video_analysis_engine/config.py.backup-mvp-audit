from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"
FRAMES_DIR = BASE_DIR / "frames_output"
AUDIO_DIR = BASE_DIR / "audio_output"
TEMP_DIR = BASE_DIR / "temp"

for folder in [UPLOAD_DIR, FRAMES_DIR, AUDIO_DIR, TEMP_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

MAX_VIDEO_SIZE_MB = 500
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

DEFAULT_FRAME_INTERVAL_SECONDS = 2
DEFAULT_MAX_FRAMES = 12

AUDIO_FORMAT = "wav"

# Gemini confi GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBmrLYFZDsOZ_zQsRjFg9n28RnWNkZPkzg")
ANALYSIS_MODEL = os.getenv("ANALYSIS_MODEL", "gemini-2.5-flash-lite")

# Google Speech-to-Text config
TRANSCRIPTION_MODEL = os.getenv("TRANSCRIPTION_MODEL", "google-cloud-speech")
TRANSCRIPTION_LANGUAGE_CODE = os.getenv("TRANSCRIPTION_LANGUAGE_CODE", "en-US")
TRANSCRIPTION_SAMPLE_RATE_HERTZ = int(os.getenv("TRANSCRIPTION_SAMPLE_RATE_HERTZ", "16000"))

OCR_ENABLED = True
OCR_LANGUAGE = "eng"

MAX_ANALYSIS_TOKENS = 1400
ANALYSIS_TEMPERATURE = 0.2

DELETE_TEMP_FILES_AFTER_ANALYSIS = True


def validate_video_extension(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_VIDEO_EXTENSIONS

# AI config from environment variables only
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANALYSIS_MODEL = os.getenv("ANALYSIS_MODEL", "gemini-2.5-flash-lite")
