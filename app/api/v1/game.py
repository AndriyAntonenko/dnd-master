from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.api.services.games_service import GamesService
from app.core.worker import queue
from app.models.game import GameSession
from app.models.game import GameSession

router = APIRouter()

class GameSessionCreate(BaseModel):
  title: str
  setting_prompt: str
  roles_system: str

@router.post("/")
async def create_game(game_in: GameSessionCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
  games_service = GamesService(db)
  # Create game entry with CREATING status
  game = await games_service.create_game(
    game_in.title,
    current_user.id
  )

  # Enqueue the task
  await queue.enqueue(
      "create_game_task",
      game_id=str(game.id),
      title=game_in.title,
      setting_prompt=game_in.setting_prompt,
      roles_system=game_in.roles_system,
      host_id=current_user.id,
      timeout=600
  )

  return game

@router.get("/{game_id}")
async def get_game_status(game_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    games_service = GamesService(db)
    game = await games_service.get_game_by_id(game_id)
    
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
        
    return game
