from app.models import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey, DateTime, Enum, Boolean
from datetime import datetime
import enum

class NotificationType(enum.Enum):
    mention = "mention"
    reply = "reply"
    announcement ="announcement"

class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type: Mapped[NotificationType] = mapped_column(Enum(NotificationType))
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    thread_id: Mapped[int] = mapped_column(ForeignKey("threads.id"), nullable=True)
    comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)