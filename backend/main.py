from fastapi import FastAPI
import asyncio
from backend.cache.redis import redis_cache
from backend.api.routers import order_router
from backend.core.config import settings
from backend.db.session import engine, Base
import backend.db.models  

app = FastAPI(title="Order Processing Backend", version="1.0")

@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    """Runs at application startup: creates tables & initializes Redis."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await redis_cache.init_cache()  # Ensure Redis is initialized

@app.on_event("shutdown")
async def shutdown():
    """Handles cleanup on shutdown."""
    if redis_cache.redis:
        await redis_cache.redis.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Order Processing Backend API!"}

# Include order router
app.include_router(order_router, prefix="/orders", tags=["Orders"])
