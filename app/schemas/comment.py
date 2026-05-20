from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    content: str
    parent_id: Optional[int] = None
    thread_id: int
    image_url: Optional[str] = None

class CommentUpdate(BaseModel):
    content: Optional[str] = None
    image_url: Optional[str] = None

class CommentReaction(BaseModel):
    value: int  # 1 или -1

class CommentResponse(BaseModel):
    id: int
    parent_id: Optional[int] = None
    content: str
    user_id: int
    thread_id: int
    rating: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_deleted: bool = False
    image_url: Optional[str] = None
    
    class Config:
        from_attributes = True