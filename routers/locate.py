import os

from fastapi import APIRouter, HTTPException
from fastapi import status

from schemas.direction import Direction
from schemas.errors import NOT_FOUND, NOT_ACCEPTABLE
from services.image import UPLOAD_IMG_DIR
from services.locate import LocateService

router = APIRouter(
    prefix="/locate",
    tags=["locate"],
)

service = LocateService()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[Direction],
    responses={**NOT_FOUND, **NOT_ACCEPTABLE},
)
def locate(
    image_name: str,
    class_name: str,
):
    if image_name not in os.listdir(UPLOAD_IMG_DIR):
        raise HTTPException(status_code=404, detail="Image not found")
    direction = service.predict(image_name, class_name)
    if not direction:
        raise HTTPException(status_code=406, detail="Class not found")
    return direction
