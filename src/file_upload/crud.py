from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth.models import User

from .models import UploadedFile
from .utils import (file_exists_by_content, file_exists_by_name,
                    is_valid_py_extension)


async def create_uploaded_file(
        db: AsyncSession,
        user: User,
        filename: str,
        content: bytes
) -> UploadedFile:

    if not is_valid_py_extension(filename):
        raise ValueError("Only .py files are allowed.")
    decoded_content = content.decode("utf-8")
    if await file_exists_by_name(db, filename):
        raise ValueError("File with the same name already exists.")
    if await file_exists_by_content(db, decoded_content):
        raise ValueError("File with the same content already exists.")

    uploaded_file = UploadedFile(
        user_id=user.id,
        filename=filename,
        content=decoded_content,
        is_new=True
    )
    db.add(uploaded_file)
    await db.commit()
    await db.refresh(uploaded_file)
    return uploaded_file


async def delete_uploaded_file(
    db: AsyncSession,
    file_id: int,
    user: User
):
    stmt = select(UploadedFile).where(
        UploadedFile.id == file_id, UploadedFile.user_id == user.id
    )
    uploaded_file = (await db.execute(stmt)).scalar_one_or_none()
    print(uploaded_file.filename)

    if not uploaded_file:
        raise ValueError("File not found or not owned by the user.")

    await db.delete(uploaded_file)
    await db.commit()


async def update_uploaded_file(
        db: AsyncSession,
        file_id: int,
        user: User,
        filename: str,
        content: str):

    stmt = select(UploadedFile).where(
        UploadedFile.id == file_id, UploadedFile.user_id == user.id
    )
    update_file = (await db.execute(stmt)).scalar_one_or_none()

    if not update_file:
        raise ValueError("File not found or not owned by the user.")

    if not is_valid_py_extension(filename):
        raise ValueError("Only .py files are allowed.")

    update_file.filename = filename
    update_file.content = content.decode("utf-8")
    update_file.is_new = False
    update_file.is_updated = True
    await db.commit()
    return update_file


async def get_user_uploaded_file(db: AsyncSession, user: User):
    stmt = select(UploadedFile).where(UploadedFile.user_id == user.id)
    result = await db.execute(stmt)
    return result.all()
