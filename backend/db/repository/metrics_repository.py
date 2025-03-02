from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.db.models.order import Order

class MetricsRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_total_orders(self):
        """Fetch total number of orders from the database."""
        result = await self.db.execute(select(Order))
        return len(result.scalars().all())
    
    async def get_pending_orders(self):
        """Fetch count of pending orders."""
        result = await self.db.execute(select(Order).where(Order.status == "Pending"))
        return len(result.scalars().all())
    
    async def get_completed_orders(self):
        """Fetch count of completed orders."""
        result = await self.db.execute(select(Order).where(Order.status == "Completed"))
        return len(result.scalars().all())
