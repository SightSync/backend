from fastapi import APIRouter
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
        audio: bytes,
):
    return service.get_transcription(audio)
