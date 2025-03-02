from fastapi import FastAPI
import asyncio

from backend.api.routers import order_router
from backend.core.config import settings
from backend.db.session import engine, Base

app = FastAPI(title="Order Processing Backend", version="1.0")
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
app.include_router(order_router.router, prefix="/orders", tags=["orders"])

# order_queue = asyncio.Queue()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Order Processing Backend API!"}
  