from app.db.session import async_session
from sqlalchemy.future import select
from app.db.models import Order

async def get_metrics():
    """Compute metrics such as total orders, status counts, and processing time."""
    async with async_session() as db:
        total_orders = await db.execute(select(Order))
        total_orders_count = len(total_orders.scalars().all())
        
        completed_orders = await db.execute(select(Order).where(Order.status == "Completed"))
        completed_count = len(completed_orders.scalars().all())

        pending_orders = await db.execute(select(Order).where(Order.status == "Pending"))
        pending_count = len(pending_orders.scalars().all())

        processing_orders = total_orders_count - (completed_count + pending_count)
        
        avg_processing_time = 0  # Implement logic for average processing time
        
        return {
            "total_orders": total_orders_count,
            "completed_orders": completed_count,
            "pending_orders": pending_count,
            "processing_orders": processing_orders,
            "avg_processing_time": avg_processing_time
        }
