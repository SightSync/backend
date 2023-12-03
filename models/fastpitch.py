import torch
from transformers import pipeline
from nemo.collections.tts.models import FastPitchModel
import soundfile as sf
from nemo.collections.tts.models import HifiGanModel
import io


class FastPitchMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(FastPitchMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FastPitch(metaclass=FastPitchMeta):
    pipe: pipeline
    spec_generator: FastPitchModel
    model: HifiGanModel

    def __init__(self):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.spec_generator = FastPitchModel.from_pretrained("nvidia/tts_en_fastpitch")
        self.spec_generator = self.spec_generator.to(device)

        self.model = HifiGanModel.from_pretrained(model_name="nvidia/tts_hifigan")
        self.model = self.model.to(device)

    def get_speech_synthesis(self, text: str) -> io.BytesIO:
        parsed = self.spec_generator.parse(text)
        spectrogram = self.spec_generator.generate_spectrogram(tokens=parsed)
        audio = self.model.convert_spectrogram_to_audio(spec=spectrogram)
        wav_file = io.BytesIO()
        sf.write(wav_file, audio.to('cpu').detach().numpy()[0], 22050, format='WAV')
        return wav_file

