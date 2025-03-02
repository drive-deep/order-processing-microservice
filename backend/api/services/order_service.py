from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.repository.order_repository import OrderRepository
from backend.schemas.order import OrderCreate, Order as OrderSchema
from backend.queue.order_queue import add_order
from backend.db.session import get_db  # Ensure you have a function to provide AsyncSession

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderSchema)
async def create_order(
    order: OrderCreate, 
    db: AsyncSession = Depends(get_db)  # Inject database session
):
    """Create a new order and add to the processing queue."""
    repository = OrderRepository(db)  # Pass db session to repository
    db_order = await repository.create_order(order)
    await add_order(db_order)
    return OrderSchema.model_validate(db_order)  # Ensure correct Pydantic serialization

@router.get("/{order_id}", response_model=OrderSchema)
async def get_order(
    order_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """Retrieve the status of an order (Uses Redis cache)."""
    repository = OrderRepository(db)
    db_order = await repository.get_order(order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderSchema.model_validate(db_order)  # Ensure correct Pydantic serialization
