from app.models.vote import Vote
from app.schemas.vote import VoteCreate
from app.services.threads import get_thread_by_id
from app.services.comments import get_comment_by_id
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

async def vote_thread(db: AsyncSession, user_id: int, thread_id: int, value: int):
    thread = await get_thread_by_id(db, thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Тред не найден")
    
    result = await db.execute(
        select(Vote).where(Vote.user_id == user_id, Vote.thread_id == thread_id)
    )
    existing_vote = result.scalar_one_or_none()

    if existing_vote:
        if existing_vote.value == value:
            thread.rating -= value
            await db.delete(existing_vote)
        else:
            thread.rating += value * 2
            existing_vote.value = value
    else:
        vote = Vote(user_id=user_id, thread_id=thread_id, value=value)
        db.add(vote)
        thread.rating += value
    await db.commit()
    await db.refresh(thread)
    return thread

async def vote_comment(db: AsyncSession, user_id: int, comment_id: int, value: int):
    comment = await get_comment_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    
    result = await db.execute(
        select(Vote).where(Vote.user_id == user_id, Vote.comment_id == comment_id)
    )
    existing_vote = result.scalar_one_or_none()

    if existing_vote:
        if existing_vote.value == value:
            comment.rating -= value
            await db.delete(existing_vote)
        else:
            comment.rating += value * 2
            existing_vote.value = value
    else:
        vote = Vote(user_id=user_id, comment_id=comment_id, value=value)
        db.add(vote)
        comment.rating += value
    await db.commit()
    await db.refresh(comment)
    return comment