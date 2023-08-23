from sqlalchemy.ext.asyncio import AsyncSession
from file_upload.models import UploadedFile
from .models import ReviewLog


async def create_review_log(
        db: AsyncSession,
        uploaded_file: UploadedFile,
        result: str):
    review_log = ReviewLog(
        uploaded_file_id=uploaded_file.id,
        result=result
    )
    db.add(review_log)
    await db.commit()
    await db.refresh(review_log)
    return review_log
