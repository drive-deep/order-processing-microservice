from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.db.models.order import Order
from backend.schemas.order import OrderCreate
from backend.cache.redis import cache_order, get_cached_order

class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_order(self, order_data: OrderCreate):
        """Create and store a new order in the database."""
        new_order = Order(**order_data.model_dump(), status="Pending")
        self.db.add(new_order)
        await self.db.commit()
        await self.db.refresh(new_order)
        
        # Cache the order in Redis for faster retrieval
        await cache_order(new_order)
        
        return new_order

    async def get_order(self, order_id: int):
        """Retrieve an order, first checking Redis cache before querying DB."""
        cached_order = await get_cached_order(order_id)
        if cached_order:
            return cached_order  # Return cached order if available
        
        # Fetch from database if not in cache
        result = await self.db.execute(select(Order).where(Order.id == order_id))
        order = result.scalars().first()
        
        # Cache the order for future requests
        if order:
            await cache_order(order)
        
        return order