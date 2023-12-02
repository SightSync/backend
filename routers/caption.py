import os

from fastapi import APIRouter, HTTPException
from fastapi import status

from schemas.errors import NOT_FOUND
from services.caption import CaptionService
from services.image import UPLOAD_IMG_DIR

router = APIRouter(
    prefix="/caption",
    tags=["caption"],
)

service = CaptionService()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=str,
    responses={**NOT_FOUND},
)
def get_caption(
    image_name: str,
    query: str,
):
    if image_name not in os.listdir(UPLOAD_IMG_DIR):
        raise HTTPException(status_code=404, detail="Image not found")
    return service.get_query(image_name, query)
