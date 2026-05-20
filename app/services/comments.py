from app.schemas.comment import CommentCreate, CommentUpdate
from app.models.comment import Comment
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

async def create_comment(db: AsyncSession, data: CommentCreate, user_id: int) -> Comment:

    comment = Comment(
        content=data.content,
        parent_id=data.parent_id,
        thread_id=data.thread_id,
        image_url=data.image_url,
        user_id=user_id
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment

async def get_comments_by_thread(db: AsyncSession, thread_id: int) -> list[Comment]:
    result = await db.execute(
        select(Comment)
        .where(Comment.thread_id == thread_id, Comment.is_deleted == False)
        .order_by(Comment.created_at.asc())
    )
    return result.scalars().all()

async def get_comment_by_id(db: AsyncSession, comment_id: int) -> Comment | None:
    result = await db.execute(
        select(Comment).where(Comment.id == comment_id, Comment.is_deleted == False)
    )
    return result.scalar_one_or_none()

async def update_comment(db: AsyncSession, comment_id: int, data: CommentUpdate) -> Comment:

    comment = await get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=404, 
            detail="Комментарий не найден"
            )

    if data.content is not None:
        comment.content = data.content
    if data.image_url is not None:
        comment.image_url = data.image_url

    await db.commit()
    await db.refresh(comment)
    return comment

async def delete_comment(db: AsyncSession, comment_id: int) -> None:
    comment = await get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    
    comment.is_deleted = True
    await db.commit()