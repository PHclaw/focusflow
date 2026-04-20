from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from ..core.database import Base
from datetime import datetime
import enum

class FocusType(str, enum.Enum):
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"

class AchievementType(str, enum.Enum):
    TOTAL_MINUTES = "total_minutes"
    DAILY_SESSIONS = "daily_sessions"
    STREAK_DAYS = "streak_days"
    TOTAL_SESSIONS = "total_sessions"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    total_focus_minutes = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    coins = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    sessions = relationship("FocusSession", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")
    unlocked_sounds = relationship("UserSound", back_populates="user")

class FocusSession(Base):
    __tablename__ = "focus_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    focus_type = Column(Enum(FocusType), default=FocusType.WORK)
    duration_minutes = Column(Integer, default=25)
    completed = Column(Boolean, default=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="sessions")

class DailyStats(Base):
    __tablename__ = "daily_stats"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, index=True)
    focus_minutes = Column(Integer, default=0)
    sessions_completed = Column(Integer, default=0)

class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    icon = Column(String)
    requirement_type = Column(Enum(AchievementType))
    requirement_value = Column(Integer)
    reward_coins = Column(Integer, default=10)

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    achievement_id = Column(Integer, ForeignKey("achievements.id"))
    earned_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="achievements")

class Sound(Base):
    __tablename__ = "sounds"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    category = Column(String)  # nature, ambient, melody
    file_path = Column(String)
    is_premium = Column(Boolean, default=False)
    price = Column(Integer, default=0)
    emoji = Column(String)

class UserSound(Base):
    __tablename__ = "user_sounds"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    sound_id = Column(Integer, ForeignKey("sounds.id"))
    
    user = relationship("User", back_populates="unlocked_sounds")
