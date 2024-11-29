from openai import OpenAI
from app.config import env

class AudioTranscriptionService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=env.openai_api_key,base_url=env.openai_base_url)
        self.openai_audio_model: str = "whisper-1"


    def get_audio_transcription(self, audio_path: str) -> str:
        # Motion G gateway not ready for openai audio transcription
        output_transcription = None
        # Transcribe the audio
        transcription = self.openai_client.audio.transcriptions.create(
            model=self.openai_audio_model,
            file=open(audio_path, "rb"),
        )
        output_transcription = transcription.text
        return output_transcription
    

# def test_audio_transcription_service():
#     audio_transcription_service = AudioTranscriptionService()
#     audio_path = "app/tests/data/test_audio.wav"
#     transcription = audio_transcription_service.get_audio_transcription(audio_path)