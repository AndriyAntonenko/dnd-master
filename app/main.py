from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import auth, text, image, audio, video

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(text.router, prefix="/api/v1/text", tags=["text"])
app.include_router(image.router, prefix="/api/v1/image", tags=["image"])
app.include_router(audio.router, prefix="/api/v1/audio", tags=["audio"])
app.include_router(video.router, prefix="/api/v1/video", tags=["video"])

@app.get("/")
async def root():
    return {"message": "Welcome to Dungeon Master AI API"}
