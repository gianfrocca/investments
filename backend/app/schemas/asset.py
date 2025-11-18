from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.asset import AssetType


class AssetBase(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20)
    name: str = Field(..., min_length=1, max_length=200)
    asset_type: AssetType
    isin: Optional[str] = None
    currency: str = "EUR"


class AssetCreate(AssetBase):
    portfolio_id: int
    quantity: float = Field(..., gt=0)
    average_buy_price: Optional[float] = Field(None, gt=0)


class AssetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    quantity: Optional[float] = Field(None, gt=0)
    average_buy_price: Optional[float] = Field(None, gt=0)
    current_price: Optional[float] = Field(None, gt=0)


class AssetStats(BaseModel):
    total_invested: float
    current_value: float
    gain_loss: float
    gain_loss_percentage: float
    total_dividends: float


class Asset(AssetBase):
    id: int
    portfolio_id: int
    quantity: float
    average_buy_price: Optional[float] = None
    current_price: Optional[float] = None
    last_price_update: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AssetWithStats(Asset):
    stats: Optional[AssetStats] = None
