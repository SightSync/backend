from fastapi import APIRouter
from fastapi import status
from fastapi.responses import FileResponse

from services.tts import TtsService

router = APIRouter(
    prefix="/tts",
    tags=["tts"],
)

service = TtsService()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "content": {"audio/wav": {}},
            "description": "Successfully generated audio",
        }
    },
)
async def get_speech_synthesis(
        text: str

):
    wav_data = service.get_speech_synthesis(text)

    filename = "sine_wave.wav"
    wav_data = wav_data.getvalue()

    with open(filename, mode="wb") as f:
        f.write(wav_data)

    return FileResponse(filename, media_type="audio/wav", filename=filename)
