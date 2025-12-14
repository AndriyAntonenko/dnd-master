from typing import Optional
from openai import AsyncOpenAI
from pydantic import BaseModel
import random
import string

import base64


from app.api.services.files_storage_service import FilesStorageService

GM_INSTRUCTIONS = """
You are a Game Master for a roleplaying game.
You should behave like a wise and experienced wizard who has a deep knowledge of fantasy literature and games.
"""

GENERATE_WORLD_CONTEXT_PROMPT = """
Your task is to generate a world context (aka Lore) for a roleplaying DnD game.

Setting prompt: {setting_prompt}
Roles system: {roles_system}

Your response should be a JSON object with the following structure:
{{
  "world_context": "The world context for the game",
  "success": true,
  "error": "Optional error message"
}}

If provided invalid setting prompt or roles system, return an error message and success flag MUST be false.
"""

GENERATE_GAME_POSTER_PROMPT = """
Your task is to generate a game poster image for a roleplaying DnD game.

World context: {world_context}
"""


class GMGenerateWorldContextResponse(BaseModel):
  world_context: str
  success: bool
  error: Optional[str] = None


class GMGenerateGamePosterResponse(BaseModel):
  game_poster: str
  success: bool
  error: Optional[str] = None


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_substring = ''.join(random.choice(characters) for i in range(length))
    return random_substring


class GM:
  def __init__(self, api_key: str):
    self.client = AsyncOpenAI(api_key=api_key)
    self.files_storage_service = FilesStorageService()

  async def generate_world_context_from_prompt(self, setting_prompt: str, roles_system: str) -> str:
    response = await self.client.beta.chat.completions.parse(
      model="gpt-4o-mini",
      messages=[
        {
          "role": "system",
          "content": GM_INSTRUCTIONS
        },
        {
          "role": "user",
          "content": GENERATE_WORLD_CONTEXT_PROMPT.format(
            setting_prompt=setting_prompt,
            roles_system=roles_system
          )
        }
      ],
      response_format=GMGenerateWorldContextResponse,
    )

    data = response.choices[0].message.parsed
    if data.success:
      return data.world_context
    else:
      raise ValueError(data.error)

  """
  This method generates a game poster based on the world context that will be attached to players game session
  and it must describe the game in a way that it will be interesting to play.
  """
  async def generate_game_poster_image(self, world_context: str) -> str:
    response = await self.client.responses.create(
      model="gpt-4.1-mini",
      input=GENERATE_GAME_POSTER_PROMPT.format(
        world_context=world_context
      ),
      tools=[{"type": "image_generation"}]
    )

    image_data = [
        output.result 
        for output in response.output
        if output.type == "image_generation_call"
    ]

    if image_data:
      file_name = "posters/game_poster_" + generate_random_string(10) + ".png"
      image_bytes = base64.b64decode(image_data[0])
      image_url: str = await self.files_storage_service.upload_file(image_bytes, file_name, "image/png")
      return image_url
    else:
      raise ValueError("Failed to generate game poster image")
