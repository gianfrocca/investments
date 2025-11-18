from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)

    # Price data
    price = Column(Float, nullable=False)
    currency = Column(String, default="EUR")

    # Timestamp
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)

    # Source of price data
    source = Column(String)  # e.g., "Alpha Vantage", "Yahoo Finance", "Manual"

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    asset = relationship("Asset", back_populates="price_history")

    # Composite index for efficient queries
    __table_args__ = (
        Index('ix_price_history_asset_timestamp', 'asset_id', 'timestamp'),
    )
