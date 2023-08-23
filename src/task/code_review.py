from celery import shared_task
from celery.utils.log import get_task_logger

from auth.models import User
from db.session import get_async_session
from file_upload.crud import get_user_uploaded_files
from review_file.utilis import run_code_review
from review_file.crud import create_review_log

logger = get_task_logger(__name__)


@shared_task
async def run_code_review_task(file_id: int, user_id: int):
    logger.info(
        f"Running code review for file_id {file_id} by user_id {user_id}"
    )
    async with get_async_session() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            uploaded_file = get_user_uploaded_files(db, user).filter_by(id=file_id).first()
            if uploaded_file:
                review_result = run_code_review(uploaded_file.content)
                create_review_log(db, uploaded_file, review_result)
                logger.info(f"Code review completed for file_id {file_id} by user_id {user_id}")
            else:
                logger.error(f"Uploaded file with id {file_id} not found for user_id {user_id}")
        else:
            logger.error(f"User with id {user_id} not found")
