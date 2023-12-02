import torch
from transformers import pipeline


class WhisperMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(WhisperMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Whisper(metaclass=WhisperMeta):
    pipe: pipeline

    def __init__(self):
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model="distil-whisper/large-v2",
            torch_dtype=torch.float16,
            device="cuda:0",
            model_kwargs={"use_flash_attention_2": True},
        )

    def get_transcription(self, audio: bytes) -> str:
        outputs = self.pipe(audio,
                            chunk_length_s=30,
                            batch_size=24,
                            return_timestamps=True)
        return outputs[0]["text"]
