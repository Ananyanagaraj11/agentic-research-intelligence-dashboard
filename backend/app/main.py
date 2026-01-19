from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.app.routers import analytics, health

app = FastAPI(title="Agentic Research Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

