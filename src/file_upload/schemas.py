from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UploadedFileCreate(BaseModel):
    filename: str
    content: str


class UploadedFileUpdate(BaseModel):
    message: str
    filename: str
    created_at: datetime


class UploadedFileResponse(BaseModel):
    message: str
    filename: Optional[str]
    created_at:  Optional[datetime]

    class Config:
        orm_mode = True


class UploadedFileGet(BaseModel):
    id: int
    filename: str
    is_new: Optional[bool]
    created_at: datetime

    class Config:
        orm_mode = True
