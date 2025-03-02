from sqlalchemy import Column, Integer, String, Float, Enum, DateTime
from backend.db.session import Base  
from datetime import datetime, timezone
import enum

class OrderStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    item_ids = Column(String)
    total_amount = Column(Float)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)  # ✅ Fix
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)
