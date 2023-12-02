import uuid

from fastapi import UploadFile

UPLOAD_IMG_DIR = "static/upload"


def save_image(image: UploadFile, extension: str):
    image_name = f"{uuid.uuid4()}.{extension}"
    image_path = f"{UPLOAD_IMG_DIR}/{image_name}"
    with open(image_path, "wb") as buffer:
        buffer.write(image.file.read())
    return image_name
