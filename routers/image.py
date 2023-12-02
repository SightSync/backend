import os

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi import status
from fastapi.responses import FileResponse

from schemas.errors import INVALID_REQUEST, NOT_FOUND
from services.image import save_image, UPLOAD_IMG_DIR

IMAGE_MIME_TYPES = ["image/jpeg", "image/png"]

router = APIRouter(
    prefix="/image",
    tags=["image"],
)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=str,
    responses={**INVALID_REQUEST},
)
async def upload_image(
    image: UploadFile = File(..., description="Image to be captioned")
):
    if image.content_type not in IMAGE_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Image must be a JPEG or PNG file")
    if image.content_type == "image/jpeg":
        return save_image(image, "jpeg")
    else:
        return save_image(image, "png")


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_class=FileResponse,
    responses={**NOT_FOUND},
)
async def get_image(image_name: str):
    if image_name not in os.listdir(UPLOAD_IMG_DIR):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(f"{UPLOAD_IMG_DIR}/{image_name}")
