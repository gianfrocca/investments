from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PortfolioBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class PortfolioStats(BaseModel):
    total_value: float
    total_invested: float
    total_gain_loss: float
    total_gain_loss_percentage: float
    asset_count: int


class Portfolio(PortfolioBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PortfolioWithStats(Portfolio):
    stats: Optional[PortfolioStats] = None
