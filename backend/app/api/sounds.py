from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..core.database import get_db
from ..api.auth import get_current_user
from ..models.models import User, Sound, UserSound

router = APIRouter(prefix="/sounds", tags=["sounds"])

@router.get("/")
async def list_sounds(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Sound))
    sounds = result.scalars().all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "category": s.category,
            "is_premium": s.is_premium,
            "price": s.price,
            "emoji": s.emoji
        }
        for s in sounds
    ]

@router.get("/unlocked")
async def get_unlocked(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Sound)
        .join(UserSound)
        .where(UserSound.user_id == user.id)
    )
    sounds = result.scalars().all()
    return [{"id": s.id, "name": s.name, "emoji": s.emoji} for s in sounds]

@router.post("/unlock/{sound_id}")
async def unlock_sound(
    sound_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    sound = await db.get(Sound, sound_id)
    if not sound:
        return {"error": "Sound not found"}
    
    if not sound.is_premium:
        return {"message": "Already free"}
    
    if user.coins < sound.price:
        return {"error": f"Not enough coins. Need {sound.price}"}
    
    result = await db.execute(
        select(UserSound).where(
            UserSound.user_id == user.id,
            UserSound.sound_id == sound_id
        )
    )
    if result.scalar_one_or_none():
        return {"message": "Already unlocked"}
    
    user.coins -= sound.price
    us = UserSound(user_id=user.id, sound_id=sound_id)
    db.add(us)
    await db.commit()
    
    return {"message": f"Unlocked {sound.name}!", "remaining_coins": user.coins}
