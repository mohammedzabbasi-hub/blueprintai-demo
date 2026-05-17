from .schemas import VideoAnalysisInput


def build_analysis_prompt(data: VideoAnalysisInput) -> str:
    frame_lines = "\n".join(
        f"- {f.timestamp_seconds}s -> {f.image_path}"
        for f in data.frames
    )

    ocr_lines = "\n".join(
        f"- {item.timestamp_seconds}s -> {item.text}"
        for item in data.ocr_text
    ) or "No OCR text detected."

    transcript_text = data.transcript.full_text or "No transcript available."

    return f"""
You are analyzing a short-form ecommerce video ad.

Evaluate the video using the metadata, extracted frame timestamps, transcript, and on-screen text.

Return ONLY valid JSON with this exact schema:
{{
  "hook_score": <integer 1-10>,
  "cta_score": <integer 1-10>,
  "clarity_score": <integer 1-10>,
  "creator_style": "<string>",
  "strengths": ["<string>", "<string>", "<string>"],
  "weaknesses": ["<string>", "<string>", "<string>"],
  "recommendations": ["<string>", "<string>", "<string>"],
  "summary": "<short paragraph>"
}}

Video metadata:
- filename: {data.metadata.filename}
- duration_seconds: {data.metadata.duration_seconds}
- resolution: {data.metadata.width}x{data.metadata.height}
- fps: {data.metadata.fps}
- aspect_ratio: {data.metadata.aspect_ratio}

Extracted frames:
{frame_lines}

Transcript:
{transcript_text}

On-screen text:
{ocr_lines}
""".strip()
