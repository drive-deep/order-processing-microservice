import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.encoders import jsonable_encoder

from backend.db.models.order import Order
from backend.schemas.order import OrderCreate
from backend.cache.redis import redis_cache
from backend.db.session import async_session_maker  # Ensure async session creation


class OrderRepository:
    async def create_order(self, order_data: OrderCreate):
        """Create and store a new order in the database."""
        async with async_session_maker() as session:  # Correct session creation
            async with session.begin():  # Ensure transaction is handled properly
                new_order = Order(**order_data.model_dump(), status="Pending")
                session.add(new_order)
                await session.flush()  # Flush to get the ID before commit

            await session.refresh(new_order)
            
            # Cache the order in Redis for faster retrieval
            order_json = json.dumps(jsonable_encoder(new_order))
            await redis_cache.set(f"order:{new_order.order_id}", order_json)
            
            return new_order

    async def get_order(self, order_id: int):
        """Retrieve an order, first checking Redis cache before querying DB."""
        cached_order = await redis_cache.get(f"order:{order_id}")
        if cached_order:
            return json.loads(cached_order)  # Deserialize JSON before returning

        async with async_session_maker() as session:
            result = await session.execute(select(Order).where(Order.order_id == order_id))
            order = result.scalars().first()
            
            # Cache the order for future requests
            if order:
                order_json = json.dumps(jsonable_encoder(order))
                await redis_cache.set(f"order:{order_id}", order_json)
            
            return order
