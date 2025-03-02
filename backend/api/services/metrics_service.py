from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from backend.db.models.order import Order
from backend.db.session import SessionLocal  # Import SessionLocal

async def get_metrics():
    """Compute metrics such as total orders, status counts, and processing time."""
    async with SessionLocal() as db:  # Create an async session
        # Get total orders count
        total_orders_count = await db.scalar(select(func.count()).select_from(Order))

        # Get order counts grouped by status
        status_counts = await db.execute(
            select(Order.status, func.count()).group_by(Order.status)
        )
        status_counts = dict(status_counts.all())  # Convert result to dict
        
        completed_count = status_counts.get("Completed", 0)
        pending_count = status_counts.get("Pending", 0)
        processing_orders = total_orders_count - (completed_count + pending_count)

        # Calculate average processing time (assuming Order has `processing_time` column)
        avg_processing_time = await db.scalar(select(func.avg(Order.processing_time))) or 0

        return {
            "total_orders": total_orders_count,
            "completed_orders": completed_count,
            "pending_orders": pending_count,
            "processing_orders": processing_orders,
            "avg_processing_time": avg_processing_time
        }
