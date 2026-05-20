from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.vote import VoteCreate
from app.schemas.thread import ThreadResponse
from app.schemas.comment import CommentResponse
from app.services.votes import vote_thread, vote_comment

router = APIRouter(tags=["votes"])

@router.post("/threads/{thread_id}/vote", response_model=ThreadResponse)
async def thread_vote(
    vote_id: int,
    data: VoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await vote_thread(db, current_user.id, thread_id, data.value)

@router.post("/comments/{comment_id}/vote", response_model=CommentResponse)
async def comment_vote(
    comment_id: int,
    data: VoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await vote_comment(db, current_user.id, comment_id, data.value)