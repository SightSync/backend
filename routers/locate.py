from fastapi import APIRouter
from fastapi import status

from schemas.errors import NOT_FOUND
from services.locate import LocateService

router = APIRouter(
    prefix="/locate",
    tags=["locate"],
)

service = LocateService()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=str,
    responses={**NOT_FOUND},
)
def locate(
    image_name: str,
    class_name: str,
):
    return service.predict(image_name, class_name)
