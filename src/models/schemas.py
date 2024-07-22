"""Pydantic models for data validation."""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


class Sale(BaseModel):
    """Sales transaction schema."""
    transaction_id: str
    customer_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    total_amount: float = Field(gt=0)
    transaction_timestamp: str
    payment_method: str
    store_id: int = Field(gt=0)
    status: str
