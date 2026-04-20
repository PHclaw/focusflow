FROM python:3.11-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

COPY frontend/package.json ./
RUN npm ci 2>/dev/null || npm install
COPY frontend/ ./
RUN npm run build

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app

COPY --from=builder /app/backend/app ./backend/app
COPY --from=builder /app/backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=builder /app/dist ./frontend/dist

ENV PYTHONPATH=/app/backend
ENV FRONTEND_PATH=/app/frontend/dist
EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
