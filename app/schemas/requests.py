from fastapi import File, UploadFile
from pydantic import BaseModel, EmailStr


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class ItemCreateRequest(BaseRequest):
    text: UploadFile = File(...)

class ItemUpdateRequest(BaseRequest):
    text: str
