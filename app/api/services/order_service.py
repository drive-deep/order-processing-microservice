from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Order
from app.schemas.order import OrderCreate
from app.cache.redis import cache_order, get_cached_order

async def create_order(db: AsyncSession, order_data: OrderCreate):
    """Create and store a new order in the database."""
    new_order = Order(**order_data.model_dump(), status="Pending")
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    
    # Cache the order in Redis for faster retrieval
    await cache_order(new_order)
    
    return new_order

async def get_order(db: AsyncSession, order_id: int):
    """Retrieve an order, first checking Redis cache before querying DB."""
    cached_order = await get_cached_order(order_id)
    if cached_order:
        return cached_order  # Return cached order if available
    
    # Fetch from database if not in cache
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    
    # Cache the order for future requests
    if order:
        await cache_order(order)
    
    return order
