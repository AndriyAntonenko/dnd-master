import asyncio
from saq import Queue
from app.core.config import settings
from app.core.db import SessionLocal
from app.api.services.games_service import GamesService
from app.models.game import GameStatus, GameSession
from sqlalchemy import select

from app.models.user import User

# Define the queue
queue = Queue.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", name="game_creation")

async def create_game_task(ctx, *, game_id: str, title: str, setting_prompt: str, roles_system: str, host_id: int):
    async with SessionLocal() as db:
        game = None
        try:
            # Fetch the game to ensure it exists and update status
            result = await db.execute(select(GameSession).where(GameSession.id == game_id))
            game = result.scalar_one_or_none()
            
            if not game:
                print(f"Game {game_id} not found")
                return

            games_service = GamesService(db)
            
            # We need to manually trigger the generation logic here
            # Since GamesService.create_game was doing everything synchronously before,
            # we might need to refactor or use parts of it.
            # However, the previous implementation of create_game was:
            # 1. Generate world context
            # 2. Generate poster
            # 3. Save to DB
            
            # Since we already created the game entry in API (with CREATING status),
            # we now just need to populate it.
            
            from app.api.domain.gm import GM
            gm = GM(api_key=settings.OPENAI_API_KEY)
            
            world_context = await gm.generate_world_context_from_prompt(setting_prompt, roles_system)
            game_poster = await gm.generate_game_poster_image(world_context)
            
            game.world_context = world_context
            game.game_poster = game_poster
            game.status = GameStatus.CREATED
            
            db.add(game)
            await db.commit()
            
        except Exception as e:
            print(f"Error creating game {game_id}: {e}")
            # Update game status to FAILED
            if game:
                game.status = GameStatus.FAILED
                db.add(game)
                await db.commit()

settings_dict = {
    "queue": queue,
    "functions": [create_game_task],
    "concurrency": 10,
}
