from app.schemas.thread import ThreadCreate, ThreadUpdate
from app.models.thread import Thread
from sqlalchemy import select
from datetime import datetime, timedelta
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

async def create_thread(db: AsyncSession, data: ThreadCreate, user_id: int) -> Thread:

    thread = Thread(
        title=data.title,
        content=data.content,
        category_id=data.category_id,
        image_url=data.image_url,
        user_id=user_id
    )
    db.add(thread)
    await db.commit()
    await db.refresh(thread)
    return thread

async def get_threads(db: AsyncSession, skip: int = 0, limit = 20) -> list[Thread]:
    result = await db.execute(
        select(Thread)
        .where(Thread.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .order_by(Thread.created_at.desc())
    )
    return result.scalars().all()

async def get_thread_by_id(db: AsyncSession, thread_id: int) -> Thread | None:
    result = await db.execute(
        select(Thread).where(Thread.id == thread_id, Thread.is_deleted == False)
    )
    return result.scalar_one_or_none()

async def update_thread(db: AsyncSession, thread_id: int, data: ThreadUpdate) -> Thread:

    thread = await get_thread_by_id(db, thread_id)
    if not thread:
        raise HTTPException(
            status_code=404, 
            detail="Тред не найден"
            )

    if data.title is not None:
        thread.title = data.title
    if data.content is not None:
        thread.content = data.content
    if data.category_id is not None:
        thread.category_id = data.category_id
    if data.image_url is not None:
        thread.image_url = data.image_url

    await db.commit()
    await db.refresh(thread)
    return thread

async def delete_thread(db: AsyncSession, thread_id: int) -> None:
    thread = await get_thread_by_id(db, thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Тред не найден")
    
    thread.is_deleted = True
    await db.commit()

async def search_threads(db: AsyncSession, q: str, skip: int = 0, limit: int = 20):
    result = await db.execute(
        select(Thread)
        .where(
            Thread.is_deleted == False,
            Thread.title.ilike(f"%{q}%")
        )
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()