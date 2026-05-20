from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, get_current_user, require_admin
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.categories import create_category, get_categories, get_category_by_id, update_category, delete_category

router = APIRouter(prefix="/category", tags=["category"])

@router.get("/", response_model=list[CategoryResponse])
async def categories_list(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
    ):
    return await get_categories(db, skip, limit)

@router.get("/{category_id}", response_model=CategoryResponse)
async def category_get(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_category_by_id(db, category_id)

@router.post("/", response_model=CategoryResponse)
async def category_write(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return await create_category(db, data, current_user.id)

@router.put("/{category_id}", response_model=CategoryResponse)
async def category_rewrite(
    category_id: int,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return await update_category(db, category_id, data)

@router.delete("/{category_id}", status_code=204)
async def category_delete(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    await delete_category(db, category_id)