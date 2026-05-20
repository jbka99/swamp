from passlib.context import CryptContext
from fastapi import HTTPException, status
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

async def register_user(db: AsyncSession, data: UserCreate) -> User:

    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже занят"
        )
    
    result = await db.execute(select(User).where(User.username == data.username))
    if result.scalar_one_or_none():
        raise  HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username уже занят"
        ) 
    
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def login_user(db: AsyncSession, email: str, password: str) -> str:

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
 
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    return create_access_token({"sub": str(user.id)})