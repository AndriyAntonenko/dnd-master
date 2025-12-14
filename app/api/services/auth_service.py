from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.user import User
from app.core import security

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, email: str, nickname: str, password: str) -> User:
        result = await self.db.execute(select(User).filter(User.email == email))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists in the system",
            )
        
        user = User(email=email, nickname=nickname, hashed_password=security.get_password_hash(password))
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def authenticate_user(self, email: str, password: str) -> User:
        result = await self.db.execute(select(User).filter(User.email == email))
        user = result.scalars().first()
        
        if not user or not security.verify_password(password, user.hashed_password):
            return None
            
        return user
