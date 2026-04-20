from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ..core.database import get_db
from ..api.auth import get_current_user
from ..models.models import User, Achievement, UserAchievement

router = APIRouter(prefix="/achievements", tags=["achievements"])

@router.get("/")
async def list_achievements(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Achievement))
    achievements = result.scalars().all()
    return [
        {
            "id": a.id,
            "name": a.name,
            "description": a.description,
            "icon": a.icon,
            "reward": a.reward_coins
        }
        for a in achievements
    ]

@router.get("/earned")
async def get_earned(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserAchievement, Achievement)
        .join(Achievement)
        .where(UserAchievement.user_id == user.id)
        .order_by(UserAchievement.earned_at.desc())
    )
    rows = result.all()
    return [
        {
            "name": a.name,
            "description": a.description,
            "icon": a.icon,
            "earned_at": ua.earned_at
        }
        for ua, a in rows
    ]
