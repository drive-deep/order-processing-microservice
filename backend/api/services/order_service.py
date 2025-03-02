from fastapi import APIRouter, Depends, HTTPException
from backend.db.repository.order_repository import OrderRepository
from backend.schemas.order import OrderCreate, Order as OrderSchema
from backend.queue.order_queue import add_order

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderSchema)
async def create_order_api(order: OrderCreate, repository: OrderRepository = Depends()):
    """Create a new order and add to the processing queue."""
    db_order = await repository.create_order(order)
    await add_order(db_order)  # Add order to queue
    return db_order

@router.get("/{order_id}", response_model=OrderSchema)
async def get_order_api(order_id: int, repository: OrderRepository = Depends()):
    """Retrieve the status of an order (Uses Redis cache)."""
    db_order = await repository.get_order(order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order