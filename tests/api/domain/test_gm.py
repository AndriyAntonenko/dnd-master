import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.api.domain.gm import GM
from app.core.config import settings

TEST_WORLD_CONTEXT_PROMPT = """
High-fantasy world of floating islands called Aethelgard. 500 years ago the surface was destroyed. Tone is gritty adventure, steampunk meets magic. Players start in 'Iron Port', a scrap-town. The main conflict is that the levitation crystals are failing, and islands are falling into the Void below. The party creates a crew of an airship.
"""

@pytest.mark.asyncio
async def test_generate_world_context_success():
    from app.core.config import settings
    
    gm = GM(api_key=settings.OPENAI_API_KEY)
    world_context = await gm.generate_world_context_from_prompt(TEST_WORLD_CONTEXT_PROMPT, "D&D 5e")
    
    print(world_context)
    assert world_context is not None
    assert len(world_context) > 0

TEST_WORLD_CONTEXT = """
In the melancholic skies of Aethelgard, a vibrant tapestry of floating islands drifts above a chaotic abyss known as the Void. Once a thriving world filled with lush landscapes and deep oceans, Aethelgard was forever changed 500 years ago when an apocalyptic event shattered the surface, obliterating civilization and casting remnants into the ethereal winds above. These fragmented islands are buoyed by ancient levitation crystals, whose power is waning, sparking a desperate race against time as more islands begin to tumble into the consuming darkness below.  

At the heart of this turbulent narrative lies Iron Port—a bustling scrap-town built upon the remnants of lost empires. Here, the air is thick with steam and magic, machines hum with arcane energy, and the clanking of metal echoes as scrap merchants and pirates barter for their survival. Iron Port is a melting pot of adventurers, scavengers, and dreamers, caught in the web of an impending tragedy.  

The people of Aethelgard look to the skies with a mixture of hope and despair, some seeking to repair the failing crystals and revitalizing the islands, while others capitalize on the chaos, adjusting their ambitions to plunder whatever pieces of knowledge lie in ancient ruins. As players venture from Iron Port, they will form a crew for a skyfaring airship, intertwining their fates amidst an unraveling mystery that holds the key to either the salvation or the utter demise of Aethelgard. Each island presents unique challenges—from weatherborne threats to pirates wielding steam-powered weaponry, and ethereal beings that haunt the remnants of the past, marking them as targets as the chase for resources intensifies.
"""

@pytest.mark.asyncio
async def test_generate_game_poster_success():
    gm = GM(api_key=settings.OPENAI_API_KEY)
    result = await gm.generate_game_poster_image(TEST_WORLD_CONTEXT)
    
    print(result)
    assert result is not None
    assert len(result) > 0
