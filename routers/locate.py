import os

from fastapi import APIRouter, HTTPException
from fastapi import status

from schemas.direction import Direction
from schemas.errors import NOT_FOUND, NOT_ACCEPTABLE
from services.image import UPLOAD_IMG_DIR
from services.intent import IntentRecognitionService
from services.locate import LocateService

router = APIRouter(
    prefix="/locate",
    tags=["locate"],
)

service = LocateService()
class_extraction_service = IntentRecognitionService()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[Direction],
    responses={**NOT_FOUND, **NOT_ACCEPTABLE},
)
def locate(
        image_name: str,
        query: str,
):
    if image_name not in os.listdir(UPLOAD_IMG_DIR):
        raise HTTPException(status_code=404, detail="Image not found")

    class_name = class_extraction_service.get_class_for(query)
    if class_name == "NO CLASS" or class_name == "":
        return "The requested item is not an object or I am not sure about which object you are looking for. Please try again with another object or rephrase your question."
    direction = service.predict(image_name, class_name)
    if not direction:
        return "The requested item is not an object or I am not sure about which object you are looking for. Please try again with another object or rephrase your question."
        # raise HTTPException(status_code=406, detail="Class not found")
    direction = direction[0]
    return "The requested item was" + class_name + ". It is located " + direction.name + "."
