from app.core.database import AsyncSessionLocal
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings
from app.models.user import User
from sqlalchemy import select
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Невалидный токен"
    )

    try:
        decoded_token = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = decoded_token.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user

async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in [UserRole.superadmin, UserRole.moderator]:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    return current_user