from pydantic import BaseModel, field_serializer, field_validator
from typing import List, Optional
from datetime import datetime
import json

class OrderBase(BaseModel):
    user_id: int
    item_ids: List[int]
    total_amount: float

    @field_serializer("item_ids")
    def serialize_item_ids(self, item_ids: List[int], _info):
        return json.dumps(item_ids)  # Store as JSON string

    @field_validator("item_ids", mode="before")
    @classmethod
    def deserialize_item_ids(cls, value):
        if isinstance(value, str):
            return json.loads(value)  # Convert JSON string to list
        return value  # If already a list, return as is

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    order_id: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

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


class MetricsResponse(BaseModel):
    total_orders_processed: int
    average_processing_time: float
    pending_orders: int
    processing_orders: int
    completed_orders: int