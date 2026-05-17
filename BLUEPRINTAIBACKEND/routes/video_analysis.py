import os
import shutil
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from video_analysis_engine.main import run_full_video_analysis

router = APIRouter(prefix="/video-analysis", tags=["video-analysis"])

UPLOAD_DIR = Path("storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/analyze")
async def analyze_video(
    file: UploadFile = File(...),
    shop_id: str | None = Form(default=None),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    allowed_extensions = {".mp4", ".mov", ".m4v", ".webm"}
    suffix = Path(file.filename).suffix.lower()

    if suffix not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported video type. Upload mp4, mov, m4v, or webm.",
        )

    safe_name = file.filename.replace("/", "_").replace("\\", "_")
    saved_path = UPLOAD_DIR / safe_name

    try:
        with saved_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = run_full_video_analysis(str(saved_path))

        return {
            "success": True,
            "filename": file.filename,
            "shop_id": shop_id,
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    finally:
        try:
            file.file.close()
        except Exception:
            pass
