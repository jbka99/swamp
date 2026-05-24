from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.services.comments import create_comment, get_comment_by_id, get_comments_by_thread, update_comment, delete_comment

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=CommentResponse)
async def comment_write(
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_comment(db, data, current_user.id)

@router.get("/{comment_id}", response_model=CommentResponse)
async def comment_get(
    comment_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_comment_by_id(db, comment_id)

@router.get("/thread/{thread_id}", response_model=list[CommentResponse])
async def comment_get_by_thread(
    thread_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_comments_by_thread(db, thread_id)

@router.put("/{comment_id}", response_model=CommentResponse)
async def comment_rewrite(
    comment_id: int,
    data: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await update_comment(db, comment_id, data)

@router.delete("/{comment_id}", status_code=204)
async def comment_delete(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await delete_comment(db, comment_id)