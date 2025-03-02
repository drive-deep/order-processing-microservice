from sqlalchemy import Column, Integer, String, Float, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

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
    status = Column(Enum("Pending", "Processing", "Completed", name="order_status"))
    created_at = Column(DateTime, default=datetime.now(datetime.timetzone.utc))
    completed_at = Column(DateTime, nullable=True)