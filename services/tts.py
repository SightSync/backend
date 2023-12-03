import io

from models.fastpitch import FastPitch


class TtsService:
    fastpitch: FastPitch

    def __init__(self):
        self.fastpitch = FastPitch()

    def get_speech_synthesis(self, text: str) -> io.BytesIO:
        return self.fastpitch.get_speech_synthesis(text)
