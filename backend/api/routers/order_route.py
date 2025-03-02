from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.session import get_db
from backend.schemas.order import OrderCreate, Order as OrderSchema
from backend.api.services.order_service import create_order, get_order
from backend.queue.order_queue import add_order, process_order

router = APIRouter()

@router.post("/", response_model=OrderSchema)
async def create_order_api(order: OrderCreate):
    """Create a new order and add to the processing queue."""
    db_order = await create_order(order)
    #await add_order(db_order)  # Add order to queue
    return db_order

@router.get("/{order_id}", response_model=OrderSchema)
async def get_order_api(order_id: int):
    """Retrieve the status of an order (Uses Redis cache)."""
    db_order = await get_order(order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
