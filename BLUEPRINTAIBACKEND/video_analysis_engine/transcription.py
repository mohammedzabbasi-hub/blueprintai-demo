from pathlib import Path
from video_analysis_engine.schemas import TranscriptData


def transcribe_audio(audio_path: Path) -> TranscriptData:
    """
    MVP-safe transcription.
    Prevents long-video transcription crashes and returns the correct schema field: full_text.
    """

    audio_path = Path(audio_path)

    if not audio_path.exists():
        return TranscriptData(
            full_text="No transcript available because no audio file was found.",
            language="en-US",
            confidence=0.0,
        )

    try:
        size_mb = audio_path.stat().st_size / (1024 * 1024)

        if size_mb > 9:
            return TranscriptData(
                full_text="Transcript skipped because this video is too long for sync transcription. Use a video under 60 seconds for full transcript analysis.",
                language="en-US",
                confidence=0.0,
            )

        from google.cloud import speech

        client = speech.SpeechClient()

        with open(audio_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            language_code="en-US",
            enable_automatic_punctuation=True,
        )

        response = client.recognize(config=config, audio=audio)

        transcript = " ".join(
            result.alternatives[0].transcript
            for result in response.results
            if result.alternatives
        )

        return TranscriptData(
            full_text=transcript or "No clear speech detected in this video.",
            language="en-US",
            confidence=0.8 if transcript else 0.0,
        )

    except Exception as e:
        return TranscriptData(
            full_text=f"Transcript unavailable during MVP analysis. Reason: {str(e)}",
            language="en-US",
            confidence=0.0,
        )
