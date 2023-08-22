from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UploadedFileCreate(BaseModel):
    filename: str
    content: str


class UploadedFileUpdate(BaseModel):
    filename: str


# class UploadedFileDelete(BaseModel):
#     filename: Optional[str]


class UploadedFileResponse(BaseModel):
    filename: str
    is_new: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UploadedFileGet(BaseModel):
    id: int
    filename: str
    is_new: Optional[bool]
    created_at: datetime

    class Config:
        orm_mode = True

class UploadedFileDeleteRequest(BaseModel):
    filename: str
