from pydantic import BaseModel, Field
from typing import List, Optional


class VideoMetadata(BaseModel):
    filename: str
    path: str
    size_bytes: int
    duration_seconds: float
    width: int
    height: int
    fps: float
    aspect_ratio: str


class FrameData(BaseModel):
    timestamp_seconds: float
    image_path: str


class TranscriptSegment(BaseModel):
    start: Optional[float] = None
    end: Optional[float] = None
    text: str


class TranscriptData(BaseModel):
    full_text: str
    segments: List[TranscriptSegment] = Field(default_factory=list)


class OCRTextItem(BaseModel):
    timestamp_seconds: float
    text: str
    image_path: str


class VideoAnalysisInput(BaseModel):
    metadata: VideoMetadata
    frames: List[FrameData]
    transcript: TranscriptData
    ocr_text: List[OCRTextItem]


class VideoAnalysisResult(BaseModel):
    hook_score: int
    cta_score: int
    clarity_score: int
    creator_style: str
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    summary: str
