from sqlalchemy.future import select
from .models import UploadedFile
from sqlalchemy.ext.asyncio import AsyncSession


def is_valid_py_extension(filename: str) -> bool:
    return filename.endswith(".py")


async def file_exists_by_name(db: AsyncSession, filename: str) -> bool:
    result = await db.execute(
        select(UploadedFile).where(UploadedFile.filename == filename)
    )
    return bool(result.scalar_one_or_none())


async def file_exists_by_content(db: AsyncSession, content: str) -> bool:
    result = await db.execute(
        select(UploadedFile).where(UploadedFile.content == content)
    )
    return bool(result.scalar_one_or_none())