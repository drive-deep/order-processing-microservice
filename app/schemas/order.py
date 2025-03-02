from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderBase(BaseModel):
    user_id: int
    item_ids: List[int]
    total_amount: float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    order_id: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class OrderStatusResponse(BaseModel):
    order_id: int
    status: str

class OrderListResponse(BaseModel):
    orders: List[Order]

class MetricsResponse(BaseModel):
    total_orders_processed: int
    average_processing_time: float
    pending_orders: int
    processing_orders: int
    completed_orders: int