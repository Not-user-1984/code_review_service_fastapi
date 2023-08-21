from sqlalchemy.orm import Session
from auth.models import User
from .models import UploadedFile
from .utils import is_valid_py_extension


def create_uploaded_file(
        db: Session, user: User, filename: str, content: str) -> UploadedFile:
    if not is_valid_py_extension(filename):
        raise ValueError("Only .py files are allowed.")

    uploaded_file = UploadedFile(
        user_id=user.id,
        filename=filename,
        content=content,  # Добавлен аргумент с содержимым файла
        is_new=True
    )

    db.add(uploaded_file)
    db.commit()
    db.refresh(uploaded_file)

    return uploaded_file



def delete_uploaded_file(
        db: Session,
        file_id: int,
        user: User):
    uploaded_file = db.query(UploadedFile).filter(
        UploadedFile.id == file_id, UploadedFile.user_id == user.id).first()
    if not uploaded_file:
        raise ValueError("File not found or not owned by the user.")

    uploaded_file.is_deleted = True
    db.commit()


def update_uploaded_file(db: Session, file_id: int, user: User, filename: str):
    uploaded_file = db.query(UploadedFile).filter(
        UploadedFile.id == file_id, UploadedFile.user_id == user.id).first()

    if not uploaded_file:
        raise ValueError("File not found or not owned by the user.")

    if not is_valid_py_extension(filename):
        raise ValueError("Only .py files are allowed.")

    uploaded_file.is_updated = True
    db.commit()


def get_user_uploaded_file(db: Session, user: User):
    return db.query(UploadedFile).filter(UploadedFile.user_id == user.id).first()