from fastapi import APIRouter
from fastapi import status

from services.intent import IntentRecognitionService

router = APIRouter(
    prefix="/intent",
    tags=["intent"],
)

service = IntentRecognitionService()


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=str,
)
def get_intent(
        query: str,
):
    return service.get_intent(query)
