

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from auth.auth import fastapi_users
from auth.models import User
from db.session import get_async_session

from .crud import (create_uploaded_file, delete_uploaded_file,
                   get_user_uploaded_file, update_uploaded_file)
from .schemas import (UploadedFileCreate, UploadedFileDeleteRequest,
                      UploadedFileResponse, UploadedFileUpdate)

router = APIRouter() 


@router.post("/upload/", response_model=UploadedFileResponse)
def upload_file(
    file: UploadFile = File(...), 
    user: User = Depends(fastapi_users.current_user()),
    db: Session = Depends(get_async_session)
):
    content = file.file.read().decode("utf-8")
    uploaded_file = create_uploaded_file(db, user, file.filename, content)
    return uploaded_file


@router.delete("/files/{file_id}/")
def delete_file(
    file_id: int,
    # uploaded_file_delete: UploadedFileDelete,
    user: User = Depends(fastapi_users.current_user()),
    db: Session = Depends(get_async_session)
):
    delete_uploaded_file(db, file_id, user)
    return {"message": "File deleted successfully."}


@router.put("/files/{file_id}/")
def update_file(
    file_id: int,
    uploaded_file_update: UploadedFileUpdate,
    user: User = Depends(fastapi_users.current_user()),
    db: Session = Depends(get_async_session)
):
    update_uploaded_file(db, file_id, user, uploaded_file_update.filename)
    return {"message": "File updated successfully."}


@router.get("/files/", response_model=UploadedFileResponse)
def get_file(
    user: User = Depends(fastapi_users.current_user()),
    db: Session = Depends(get_async_session)
):
    uploaded_file = get_user_uploaded_file(db, user)

    if uploaded_file:
        file_response = UploadedFileResponse(
            filename=uploaded_file.filename,
            is_new=uploaded_file.is_new,
            created_at=uploaded_file.created_at
        )
        return file_response
    else:
        return None
