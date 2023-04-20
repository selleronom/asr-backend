import uuid

from pydantic import BaseModel


class BaseResponse(BaseModel):
    # may define additional fields or config shared across responses
    class Config:
        orm_mode = True


class ItemResponse(BaseResponse):
    id: int
    text: str
    user_id: uuid.UUID
