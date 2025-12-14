import uuid
import random
import string
import enum
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base

class GameStatus(str, enum.Enum):
    CREATING = "CREATING"
    CREATED = "CREATED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

game_players = Table(
    "game_players",
    Base.metadata,
    Column("game_id", UUID(as_uuid=True), ForeignKey("game_sessions.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
)

class GameSession(Base):
    __tablename__ = "game_sessions"
  
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    invite_code = Column(String, unique=True, nullable=False, default=generate_invite_code)
    status = Column(Enum(GameStatus), default=GameStatus.CREATING, nullable=False)
    setting_prompt = Column(Text, nullable=True)
    world_context = Column(Text, nullable=True)
    game_poster = Column(String, nullable=True)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    host = relationship("User", back_populates="hosted_games")
    players = relationship("User", secondary=game_players, back_populates="joined_games")
