from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.order import OrderCreate, Order as OrderSchema
from app.api.services.order_service import create_order, get_order
from app.queue.order_queue import order_queue

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderSchema)
async def create_order_api(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    """Create a new order and add to the processing queue."""
    db_order = await create_order(db, order)
    await order_queue.put(db_order)  # Add order to queue
    return db_order

@router.get("/{order_id}", response_model=OrderSchema)
async def get_order_api(order_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve the status of an order (Uses Redis cache)."""
    db_order = await get_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
