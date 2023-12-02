import io

import torchaudio
from fastapi import APIRouter, File, UploadFile
from fastapi import status

from services.stt import SttService

router = APIRouter(
    prefix="/stt",
    tags=["stt"],
)

service = SttService()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=str,
)
def get_transcription(
        audio: UploadFile = File(...),
):
    waveform, sample_rate = torchaudio.load(io.BytesIO(audio.file.read()))
    audio_tensor = waveform.numpy()[0]
    return service.get_transcription(audio_tensor)
