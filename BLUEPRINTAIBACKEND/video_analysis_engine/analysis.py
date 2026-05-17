import json
from pathlib import Path
from google import genai

from .config import (
    GEMINI_API_KEY,
    ANALYSIS_MODEL,
)
from .metadata import extract_video_metadata
from .frames import extract_key_frames
from .audio import extract_audio
from .transcription import transcribe_audio
from .ocr import extract_ocr_text
from .prompt_builder import build_analysis_prompt
from .schemas import VideoAnalysisInput, VideoAnalysisResult


def analyze_structured_video(data: VideoAnalysisInput) -> VideoAnalysisResult:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set.")

    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = build_analysis_prompt(data)

    response = client.models.generate_content(
        model=ANALYSIS_MODEL,
        contents=prompt,
    )

    raw_text = (response.text or "").strip()

    if raw_text.startswith("```json"):
        raw_text = raw_text.removeprefix("```json").strip()
    if raw_text.endswith("```"):
        raw_text = raw_text.removesuffix("```").strip()

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model returned invalid JSON: {raw_text}") from e

    return VideoAnalysisResult(**parsed)


def run_full_video_analysis(video_path: str | Path) -> dict:
    video_path = Path(video_path)

    metadata = extract_video_metadata(video_path)
    frames = extract_key_frames(video_path)
    audio_path = extract_audio(video_path)
    transcript = transcribe_audio(audio_path)
    ocr_text = extract_ocr_text(frames)

    analysis_input = VideoAnalysisInput(
        metadata=metadata,
        frames=frames,
        transcript=transcript,
        ocr_text=ocr_text,
    )

    result = analyze_structured_video(analysis_input)

    return {
        "metadata": metadata.model_dump(),
        "frames": [frame.model_dump() for frame in frames],
        "transcript": transcript.model_dump(),
        "ocr_text": [item.model_dump() for item in ocr_text],
        "analysis": result.model_dump(),
    }
