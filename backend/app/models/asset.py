from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class AssetType(str, enum.Enum):
    STOCK = "stock"
    ETF = "etf"
    CRYPTO = "crypto"
    BOND = "bond"
    COMMODITY = "commodity"
    OTHER = "other"


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)

    # Asset identification
    symbol = Column(String, nullable=False, index=True)  # Ticker symbol (e.g., AAPL, BTC)
    name = Column(String, nullable=False)  # Full name
    asset_type = Column(Enum(AssetType), nullable=False)
    isin = Column(String, index=True)  # International Securities Identification Number

    # Holdings
    quantity = Column(Float, nullable=False, default=0.0)  # Number of shares/units
    average_buy_price = Column(Float)  # Average purchase price

    # Current market data
    current_price = Column(Float)  # Latest market price
    currency = Column(String, default="EUR")

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_price_update = Column(DateTime(timezone=True))

    # Relationships
    portfolio = relationship("Portfolio", back_populates="assets")
    transactions = relationship("Transaction", back_populates="asset", cascade="all, delete-orphan")
    price_history = relationship("PriceHistory", back_populates="asset", cascade="all, delete-orphan")
