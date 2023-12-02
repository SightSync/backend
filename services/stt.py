from torch import Tensor

from models.whisper import Whisper


class SttService:
    whisper: Whisper

    def __init__(self):
        self.whisper = Whisper()

    def get_transcription(self, audio: Tensor) -> str:
        return self.whisper.get_transcription(audio)
