from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.models.category import Category
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

async def create_category(db: AsyncSession, data: CategoryCreate, user_id: int) -> Category:

    category = Category(
        name=data.name,
        description=data.description,
        color=data.color,
        image_url=data.image_url
    )
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category

async def get_categories(db: AsyncSession, skip: int = 0, limit = 20) -> list[Category]:
    result = await db.execute(
        select(Category)
        .where(Category.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .order_by(Category.created_at.desc())
    )
    return result.scalars().all()

async def get_category_by_id(db: AsyncSession, category_id: int) -> Category | None:
    result = await db.execute(
        select(Category).where(
            Category.id == category_id,
            Category.is_deleted == False
            )
    )
    return result.scalar_one_or_none()

async def update_category(db: AsyncSession, category_id: int, data: CategoryUpdate) -> Category:

    category = await get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=404, 
            detail="Категория не найдена"
            )

    if data.name is not None:
        category.name = data.name
    if data.description is not None:
        category.description = data.description
    if data.color is not None:
        category.color = data.color
    if data.image_url is not None:
        category.image_url = data.image_url

    await db.commit()
    await db.refresh(category)
    return category

async def delete_category(db: AsyncSession, category_id: int) -> None:
    category = await get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    from sqlalchemy import update
    from app.models.thread import Thread
    await db.execute(
        update(Thread)
        .where(Thread.category_id == category_id)
        .values(is_deleted=True)
    )

    category.is_deleted = True
    await db.commit()