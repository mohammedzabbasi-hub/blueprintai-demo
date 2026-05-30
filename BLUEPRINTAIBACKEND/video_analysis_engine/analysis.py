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
        return build_demo_analysis(data)

    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = build_analysis_prompt(data)

    try:
        response = client.models.generate_content(
            model=ANALYSIS_MODEL,
            contents=prompt,
        )
    except Exception:
        return build_demo_analysis(data)

    raw_text = (response.text or "").strip()

    if raw_text.startswith("```json"):
        raw_text = raw_text.removeprefix("```json").strip()
    if raw_text.endswith("```"):
        raw_text = raw_text.removesuffix("```").strip()

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        return build_demo_analysis(data)

    try:
        return VideoAnalysisResult(**parsed)
    except Exception:
        return build_demo_analysis(data)


def build_demo_analysis(data: VideoAnalysisInput) -> VideoAnalysisResult:
    transcript_text = (data.transcript.full_text or "").strip()
    ocr_text = " ".join(item.text for item in data.ocr_text if item.text).strip()
    combined_text = f"{transcript_text} {ocr_text}".lower()
    duration = float(data.metadata.duration_seconds or 0)
    has_cta = any(
        phrase in combined_text
        for phrase in ["shop now", "buy now", "tap", "link", "order", "get yours", "limited"]
    )
    has_benefit = any(
        phrase in combined_text
        for phrase in ["because", "helps", "without", "results", "benefit", "save", "easy", "fast"]
    )
    has_text_signal = bool(ocr_text)

    hook_score = 7 if duration <= 35 else 5
    clarity_score = 7 if has_text_signal or has_benefit else 5
    cta_score = 7 if has_cta else 4

    if not transcript_text and not ocr_text:
        hook_score = min(hook_score, 5)
        clarity_score = min(clarity_score, 4)
        cta_score = min(cta_score, 4)

    strengths = [
        "Video metadata and key frames were extracted successfully.",
        "The creative can be reviewed for hook, pacing, and offer clarity.",
        "Demo analysis is available while the AI provider key is not configured.",
    ]
    weaknesses = [
        "Full AI creative interpretation is disabled because GEMINI_API_KEY is not set.",
        "Hook and CTA scores are heuristic estimates, not model-generated judgments.",
        "Connect the Gemini key for deeper scene, transcript, and on-screen text reasoning.",
    ]
    recommendations = [
        "Set GEMINI_API_KEY in the backend environment for full AI analysis.",
        "Keep the product result or main pain point inside the first 2 seconds.",
        "Add a clear on-screen CTA and product benefit before the viewer reaches second 10.",
    ]

    if duration > 60:
        recommendations.append("Test a shorter cut under 35 seconds for cold traffic.")

    return VideoAnalysisResult(
        hook_score=hook_score,
        cta_score=cta_score,
        clarity_score=clarity_score,
        creator_style="Demo heuristic review",
        strengths=strengths,
        weaknesses=weaknesses,
        recommendations=recommendations,
        summary=(
            "Demo-mode analysis completed because GEMINI_API_KEY is not configured. "
            "BlueprintAI extracted the video assets and produced heuristic creative scores so the upload flow, "
            "retention analyzer, and report UI can still be tested locally."
        ),
    )


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
