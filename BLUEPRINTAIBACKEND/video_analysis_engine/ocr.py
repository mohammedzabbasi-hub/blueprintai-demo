from pathlib import Path
import pytesseract
from PIL import Image
from .config import OCR_ENABLED, OCR_LANGUAGE
from .schemas import FrameData, OCRTextItem


def extract_ocr_text(frames: list[FrameData]) -> list[OCRTextItem]:
    if not OCR_ENABLED:
        return []

    results: list[OCRTextItem] = []

    for frame in frames:
        image_path = Path(frame.image_path)
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=OCR_LANGUAGE).strip()
            if text:
                results.append(
                    OCRTextItem(
                        timestamp_seconds=frame.timestamp_seconds,
                        text=text,
                        image_path=frame.image_path,
                    )
                )
        except Exception:
            continue

    return results
