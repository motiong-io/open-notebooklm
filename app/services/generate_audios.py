import time
from bark import SAMPLE_RATE, generate_audio
from scipy.io.wavfile import write as write_wav



def generate_podcast_audio(
    text: str, speaker: str, language: str, use_advanced_audio: bool, random_voice_number: int,index:int=None
) -> str:
    """Generate audio for podcast using TTS or advanced audio models."""
    if use_advanced_audio:
        return _use_suno_model(text, speaker, language, random_voice_number,index)
    else:
        from app.services.hf_audio import _use_melotts_api
        return _use_melotts_api(text, speaker, language)


def _use_suno_model(text: str, speaker: str, language: str, random_voice_number: int,index:int = None) -> str:
    """Generate advanced audio using Bark."""
    host_voice_num = str(random_voice_number)
    guest_voice_num = str(random_voice_number + 1)
    audio_array = generate_audio(
        text,
        history_prompt=f"v2/{language}_speaker_{host_voice_num if speaker == 'Host (MotionG Host)' else guest_voice_num}",
    )
    file_path = f"app/output/audio_{language}_{speaker}.mp3"
    if index is not None:
        file_path = f"app/output/audio_{language}_{speaker}_{str(index)}.mp3"
    write_wav(file_path, SAMPLE_RATE, audio_array)
    return file_path


