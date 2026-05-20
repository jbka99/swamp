from app.models import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey

class Vote(Base):
    __tablename__ = "votes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    thread_id: Mapped[int] = mapped_column(ForeignKey("threads.id"), nullable=True)
    comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id"), nullable=True)
    value: Mapped[int] = mapped_column(Integer)