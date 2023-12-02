from pydantic import BaseModel


class DetailResponseBody(BaseModel):
    detail: str


INVALID_REQUEST = {
    400: {"description": "Error: Invalid Request", "model": DetailResponseBody}
}
NOT_FOUND = {404: {"description": "Error: Not Found", "model": DetailResponseBody}}
