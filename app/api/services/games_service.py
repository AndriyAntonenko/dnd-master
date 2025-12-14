from sqlalchemy.ext.asyncio import AsyncSession
from app.models.game import GameSession, GameStatus
from sqlalchemy import select
from app.api.domain.gm import GM
from app.core.config import settings

class GamesService:
  def __init__(self, db: AsyncSession):
    self.db = db

  async def create_game(self, title: str, host_id: int):
    game = GameSession(
      title=title,
      host_id=host_id,
      status=GameStatus.CREATING.value
    )
    self.db.add(game)
    await self.db.commit()
    await self.db.refresh(game)
    return game

  async def get_game_by_id(self, game_id: str) -> GameSession:
    result = await self.db.execute(select(GameSession).where(GameSession.id == game_id))
    return result.scalar_one_or_none()
