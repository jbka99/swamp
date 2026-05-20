from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ThreadCreate(BaseModel):
    title: str
    content: str
    category_id: int
    image_url: Optional[str] = None

class ThreadUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None

class ThreadReaction(BaseModel):
    value: int  # 1 или -1

class ThreadResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    category_id: int
    views: int
    rating: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_deleted: bool = False
    image_url: Optional[str] = None
    
    class Config:
        from_attributes = True