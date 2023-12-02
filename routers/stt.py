import os
import uuid

from fastapi import APIRouter, File, UploadFile
from fastapi import status

from services.stt import SttService

router = APIRouter(
    prefix="/stt",
    tags=["stt"],
)

service = SttService()

TEMP_UPLOAD_DIR = "temp"
os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=str,
)
def get_transcription(
        audio: UploadFile = File(...),
):
    temp_filename = str(uuid.uuid4()) + ".mp3"
    temp_file_path = os.path.join(TEMP_UPLOAD_DIR, temp_filename)
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(audio.file.read())
    transcription = service.get_transcription(temp_file_path)
    os.remove(temp_file_path)
    return transcription
