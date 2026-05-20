from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import engine
from app.routes.auth import router as auth_router
from app.routes.threads import router as thread_router
from app.routes.categories import router as categories_router
from app.routes.comments import router as comment_router
from app.routes.votes import router as vote_router
from app.routes.users import router as user_router

@asynccontextmanager
async def lifespan(app):
    async with engine.begin() as conn:
        print("БД подключена.")
    yield
    await engine.dispose()
    print("БД отключена.")

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(thread_router)
app.include_router(comment_router)
app.include_router(vote_router)
app.include_router(user_router)