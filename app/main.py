from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import auth, game

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(game.router, prefix="/api/v1/game", tags=["game"])

@app.on_event("startup")
async def startup():
    from app.core.worker import queue
    await queue.connect()

@app.get("/")
async def root():
    return {"message": "Welcome to Dungeon Master AI API"}
