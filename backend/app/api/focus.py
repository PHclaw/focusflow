from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from datetime import datetime, date, timedelta
from ..core.database import get_db
from ..api.auth import get_current_user
from ..models.models import User, FocusSession, DailyStats, Achievement, UserAchievement, AchievementType, FocusType
from ..schemas.focus import FocusSessionCreate, FocusSessionOut, FocusComplete, DailyStatsOut

router = APIRouter(prefix="/focus", tags=["focus"])

@router.post("/start", response_model=FocusSessionOut)
async def start_session(
    data: FocusSessionCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    session = FocusSession(
        user_id=user.id,
        focus_type=data.focus_type,
        duration_minutes=data.duration_minutes
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session

@router.post("/complete")
async def complete_session(
    session_id: int,
    completed: bool = True,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    session = await db.get(FocusSession, session_id)
    if not session or session.user_id != user.id:
        raise HTTPException(404, "Session not found")
    
    session.completed = completed
    session.ended_at = datetime.utcnow()
    
    if completed and session.focus_type == FocusType.WORK:
        # Update user stats
        user.total_focus_minutes += session.duration_minutes
        user.coins += session.duration_minutes  # 1 coin per minute
        
        # Update daily stats
        today = date.today()
        result = await db.execute(
            select(DailyStats).where(
                DailyStats.user_id == user.id,
                DailyStats.date >= datetime.combine(today, datetime.min.time())
            )
        )
        daily = result.scalar_one_or_none()
        
        if not daily:
            daily = DailyStats(user_id=user.id, date=datetime.utcnow())
            db.add(daily)
        
        daily.focus_minutes += session.duration_minutes
        daily.sessions_completed += 1
        
        # Check achievements
        await check_achievements(user, db)
    
    await db.commit()
    return {
        "message": "Session completed!",
        "focus_minutes": session.duration_minutes,
        "coins_earned": session.duration_minutes if completed else 0
    }

async def check_achievements(user: User, db: AsyncSession):
    result = await db.execute(select(Achievement))
    achievements = result.scalars().all()
    
    for ach in achievements:
        # Check if already earned
        result = await db.execute(
            select(UserAchievement).where(
                UserAchievement.user_id == user.id,
                UserAchievement.achievement_id == ach.id
            )
        )
        if result.scalar_one_or_none():
            continue
        
        earned = False
        
        if ach.requirement_type == AchievementType.TOTAL_MINUTES:
            earned = user.total_focus_minutes >= ach.requirement_value
        elif ach.requirement_type == AchievementType.TOTAL_SESSIONS:
            result = await db.execute(
                select(func.count(FocusSession.id)).where(
                    FocusSession.user_id == user.id,
                    FocusSession.completed == True
                )
            )
            count = result.scalar()
            earned = count >= ach.requirement_value
        
        if earned:
            ua = UserAchievement(user_id=user.id, achievement_id=ach.id)
            db.add(ua)
            user.coins += ach.reward_coins

@router.get("/stats/daily")
async def get_daily_stats(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Last 7 days
    result = await db.execute(
        select(DailyStats)
        .where(DailyStats.user_id == user.id)
        .order_by(DailyStats.date.desc())
        .limit(7)
    )
    stats = result.scalars().all()
    return [{"date": s.date, "focus_minutes": s.focus_minutes, "sessions": s.sessions_completed} for s in stats]

@router.get("/stats/weekly")
async def get_weekly_stats(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    week_ago = datetime.utcnow() - timedelta(days=7)
    result = await db.execute(
        select(func.sum(DailyStats.focus_minutes), func.sum(DailyStats.sessions_completed))
        .where(
            DailyStats.user_id == user.id,
            DailyStats.date >= week_ago
        )
    )
    minutes, sessions = result.one()
    return {
        "total_minutes": minutes or 0,
        "total_sessions": sessions or 0,
        "avg_daily": (minutes or 0) / 7
    }
