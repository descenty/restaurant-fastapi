from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.router import api_router
from core.config import settings
from db.init_db import init_db

app = FastAPI(title=settings.app_title)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def init_tables():
    await init_db()


app.include_router(api_router, prefix="/api")
