from fastapi import APIRouter
from fastapi import status

router = APIRouter(
    prefix="/caption",
    tags=["caption"],
)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=str,
)
async def get_caption():
    return {"message": "Hello World"}
