from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nickname = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    hosted_games = relationship("GameSession", back_populates="host")
    joined_games = relationship("GameSession", secondary="game_players", back_populates="players")
