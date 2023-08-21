from pydantic import BaseModel
from typing import Optional


class UploadedFileCreate(BaseModel):
    filename: str
    content: str


class UploadedFileUpdate(BaseModel):
    filename: str
    content: str


# class UploadedFileDelete(BaseModel):
#     filename: Optional[str]


class UploadedFileResponse(BaseModel):

    user_id: int
    filename: str
    is_new: bool


class UploadedFileDeleteRequest(BaseModel):
    filename: str
