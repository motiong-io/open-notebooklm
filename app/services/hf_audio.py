import time
from app.constants import MELO_API_NAME,MELO_RETRY_ATTEMPTS,MELO_RETRY_DELAY,MELO_TTS_SPACES_ID
from gradio_client import Client
from bark import SAMPLE_RATE, generate_audio, preload_models

hf_client = Client(MELO_TTS_SPACES_ID)
preload_models()


def _use_melotts_api(text: str, speaker: str, language: str) -> str:
    """Generate audio using TTS model."""
    accent, speed = _get_melo_tts_params(speaker, language)

    for attempt in range(MELO_RETRY_ATTEMPTS):
        try:
            return hf_client.predict(
                text=text,
                language=language,
                speaker=accent,
                speed=speed,
                api_name=MELO_API_NAME,
            )
        except Exception as e:
            if attempt == MELO_RETRY_ATTEMPTS - 1:  # Last attempt
                raise  # Re-raise the last exception if all attempts fail
            time.sleep(MELO_RETRY_DELAY)  # Wait for X second before retrying


def _get_melo_tts_params(speaker: str, language: str) -> tuple[str, float]:
    """Get TTS parameters based on speaker and language."""
    if speaker == "Guest":
        accent = "EN-US" if language == "EN" else language
        speed = 0.9
    else:  # host
        accent = "EN-Default" if language == "EN" else language
        speed = (
            1.1 if language != "EN" else 1
        )  # if the language is not English, try speeding up so it'll sound different from the host
        # for non-English, there is only one voice
    return accent, speed
