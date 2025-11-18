from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.transaction import TransactionType


class TransactionBase(BaseModel):
    asset_id: int
    transaction_type: TransactionType
    quantity: float = Field(..., gt=0)
    price_per_unit: float = Field(..., gt=0)
    fees: float = Field(default=0.0, ge=0)
    currency: str = "EUR"
    transaction_date: datetime
    notes: Optional[str] = None


class TransactionCreate(TransactionBase):
    portfolio_id: int
    source: Optional[str] = "Manual"
    external_id: Optional[str] = None


class Transaction(TransactionBase):
    id: int
    portfolio_id: int
    total_amount: float
    source: Optional[str] = None
    external_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TransactionWithAsset(Transaction):
    asset_symbol: str
    asset_name: str
