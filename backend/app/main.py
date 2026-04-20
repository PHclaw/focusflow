from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import init_db
from .api import auth, focus, sounds, achievements
from .models.models import Achievement, Sound
import asyncio

app = FastAPI(title="FocusFlow", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_db()
    await seed_achievements()
    await seed_sounds()

async def seed_achievements():
    from .core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        achievements = [
            Achievement(name="First Focus", description="Complete your first session", icon="馃幆", requirement_type="total_sessions", requirement_value=1, reward_coins=10),
            Achievement(name="Getting Started", description="Focus for 30 minutes total", icon="鈴?, requirement_type="total_minutes", requirement_value=30, reward_coins=20),
            Achievement(name="Deep Work", description="Focus for 2 hours total", icon="馃", requirement_type="total_minutes", requirement_value=120, reward_coins=50),
            Achievement(name="Flow State", description="Focus for 5 hours total", icon="馃寠", requirement_type="total_minutes", requirement_value=300, reward_coins=100),
            Achievement(name="Productivity Master", description="Complete 20 sessions", icon="馃弳", requirement_type="total_sessions", requirement_value=20, reward_coins=150),
            Achievement(name="Focus Legend", description="Focus for 10 hours total", icon="馃憫", requirement_type="total_minutes", requirement_value=600, reward_coins=200),
        ]
        for ach in achievements:
            result = await db.execute(select(Achievement).where(Achievement.name == ach.name))
            if not result.scalar_one_or_none():
                db.add(ach)
        await db.commit()

async def seed_sounds():
    from .core.database import AsyncSessionLocal
    async with AsyncSessionLocal() as db:
        sounds = [
            Sound(name="Rain", category="nature", file_path="/sounds/rain.mp3", is_premium=False, emoji="馃導锔?),
            Sound(name="Forest", category="nature", file_path="/sounds/forest.mp3", is_premium=False, emoji="馃尣"),
            Sound(name="Ocean", category="nature", file_path="/sounds/ocean.mp3", is_premium=False, emoji="馃寠"),
            Sound(name="Caf茅", category="ambient", file_path="/sounds/cafe.mp3", is_premium=True, price=50, emoji="鈽?),
            Sound(name="Fireplace", category="nature", file_path="/sounds/fire.mp3", is_premium=True, price=30, emoji="馃敟"),
            Sound(name="Lo-Fi Beats", category="melody", file_path="/sounds/lofi.mp3", is_premium=True, price=100, emoji="馃幍"),
            Sound(name="Wind", category="nature", file_path="/sounds/wind.mp3", is_premium=False, emoji="馃挩"),
            Sound(name="Night", category="ambient", file_path="/sounds/night.mp3", is_premium=True, price=40, emoji="馃寵"),
        ]
        for s in sounds:
            result = await db.execute(select(Sound).where(Sound.name == s.name))
            if not result.scalar_one_or_none():
                db.add(s)
        await db.commit()

app.include_router(auth.router, prefix="/api")
app.include_router(focus.router, prefix="/api")
app.include_router(sounds.router, prefix="/api")
app.include_router(achievements.router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok"}
