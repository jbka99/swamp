from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.thread import ThreadCreate, ThreadUpdate, ThreadResponse
from app.services.threads import create_thread, get_threads, get_thread_by_id, update_thread, delete_thread, search_threads

router = APIRouter(prefix="/threads", tags=["threads"])

@router.post("/", response_model=ThreadResponse)
async def thread_write(
    data: ThreadCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await create_thread(db, data, current_user.id)

@router.get("/", response_model=list[ThreadResponse])
async def threads_list(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    return await get_threads(db, skip, limit)

@router.get("/search", response_model=list[ThreadResponse])
async def thread_search(
    q: str,
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    return await search_threads(db, q, skip, limit)

@router.get("/{thread_id}", response_model=ThreadResponse)
async def thread_get(
    thread_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_thread_by_id(db, thread_id)

@router.put("/{thread_id}", response_model=ThreadResponse)
async def thread_rewrite(
    thread_id: int,
    data: ThreadUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await update_thread(db, thread_id, data)

@router.delete("/{thread_id}", status_code=204)
async def thread_delete(
    thread_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await delete_thread(db, thread_id)