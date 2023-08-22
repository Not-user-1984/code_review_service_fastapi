from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import fastapi_users
from auth.models import User
from db.session import get_async_session

from .crud import (create_uploaded_file, delete_uploaded_file,
                   get_user_uploaded_file, update_uploaded_file)
from .schemas import (UploadedFileDeleteRequest, UploadedFileGet,
                      UploadedFileResponse, UploadedFileUpdate)

router = APIRouter()


@router.post("/upload/", response_model=UploadedFileResponse)
async def upload_file(
    file: UploadFile = File(...),
    user: User = Depends(fastapi_users.current_user()),
    db: AsyncSession = Depends(get_async_session)
):
    content = await file.read()
    uploaded_file = await create_uploaded_file(
        db, user, file.filename, content)
    return uploaded_file


@router.delete("/files/{file_id}/")
async def delete_file(
    file_id: int,
    user: User = Depends(fastapi_users.current_user()),
    db: AsyncSession = Depends(get_async_session)
):
    await delete_uploaded_file(db, file_id, user)
    return {"message": "File deleted successfully."}


@router.put("/files/{file_id}/",)
async def update_file(
    file_id: int,
    user: User = Depends(fastapi_users.current_user()),
    db: AsyncSession = Depends(get_async_session),
    file: UploadFile = File(...),
):
    content = await file.read()
    await update_uploaded_file(
        db, file_id,
        user,
        file.filename,
        content
        )
    return {"message": "File updated successfully."}


@router.get("/files/", response_model=List[UploadedFileGet])
async def get_file(
    user: User = Depends(fastapi_users.current_user()),
    db: AsyncSession = Depends(get_async_session)
):
    uploaded_files = await get_user_uploaded_file(db, user)

    uploaded_file_responses = [
        UploadedFileGet(
            id=uploaded_file_item[0].id,
            filename=uploaded_file_item[0].filename,
            is_new=uploaded_file_item[0].is_new,
            created_at=uploaded_file_item[0].created_at
        )
        for uploaded_file_item in uploaded_files]
    return uploaded_file_responses
