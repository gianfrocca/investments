from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PriceUpdate(BaseModel):
    asset_id: int
    price: float = Field(..., gt=0)
    currency: str = "EUR"
    source: Optional[str] = "Manual"


class PriceHistoryPoint(BaseModel):
    timestamp: datetime
    price: float
    source: Optional[str] = None


class PriceHistoryResponse(BaseModel):
    asset_id: int
    symbol: str
    history: List[PriceHistoryPoint]

    class Config:
        from_attributes = True
