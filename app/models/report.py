from app.models import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey, DateTime, Boolean, Text, String
from datetime import datetime


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    thread_id: Mapped[int] = mapped_column(ForeignKey("threads.id"), nullable=True)
    comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id"), nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False) 
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)