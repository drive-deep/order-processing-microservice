from sqlalchemy import Column, Integer, String, Float, Enum, DateTime
from backend.db.session import Base  
from datetime import datetime, timezone
from sqlalchemy.sql import func
import enum

class OrderStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    item_ids = Column(String, nullable=False)
    total_amount = Column(Float)
    status = Column(String, default=OrderStatus.pending)
    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime, nullable=True)
