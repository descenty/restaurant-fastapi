import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.router import api_router
from cache.redis import redis_client
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
async def startup():
    await init_db()
    redis_client()


app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
