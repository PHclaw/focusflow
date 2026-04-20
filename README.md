# FocusFlow - Gamified Pomodoro Timer

> Focus better, achieve more. A beautiful timer with ambient sounds and achievements.

## Features

- **Pomodoro Timer** - Customizable work/break durations (25/5, 30/10, 45/15, 60/20)
- **Ambient Sounds** - Rain, forest, ocean, caf茅, fireplace (free & premium)
- **Achievement System** - Unlock badges for focus milestones
- **Focus Coins** - Earn coins for every minute focused
- **Streak Tracking** - Build a daily focus habit
- **Stats Dashboard** - Visualize your productivity over time

## Tech Stack

- Backend: FastAPI + PostgreSQL + SQLAlchemy
- Frontend: React 18 + Vite + TypeScript + Tailwind CSS
- Deploy: Docker + Railway

## Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key

## License

MIT
