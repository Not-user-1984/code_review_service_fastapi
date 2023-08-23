from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.base import Base


class ReviewLog(Base):
    __tablename__ = "review_logs"
    id = Column(Integer, primary_key=True, index=True)
    uploaded_file_id = Column(Integer, ForeignKey("uploaded_files.id"))
    result = Column(String)
    report_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    uploaded_file = relationship("UploadedFile", backref="review_logs")
