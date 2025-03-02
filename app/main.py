from fastapi import FastAPI
from app.api.router import orders_router
from app.core.config import settings
from app.db.session import engine, Base
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = FastAPI(title="Order Processing Backend", version="1.0")
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
app.include_router(orders_router, prefix="/orders", tags=["orders"])

order_queue = asyncio.Queue()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Order Processing Backend API!"}
  