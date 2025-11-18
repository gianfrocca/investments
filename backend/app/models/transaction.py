from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class TransactionType(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"
    DIVIDEND = "dividend"
    FEE = "fee"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)

    # Transaction details
    transaction_type = Column(Enum(TransactionType), nullable=False)
    quantity = Column(Float, nullable=False)  # Number of shares/units
    price_per_unit = Column(Float, nullable=False)  # Price per share at transaction
    total_amount = Column(Float, nullable=False)  # Total transaction value
    fees = Column(Float, default=0.0)  # Transaction fees
    currency = Column(String, default="EUR")

    # Metadata
    transaction_date = Column(DateTime(timezone=True), nullable=False)
    notes = Column(Text)
    source = Column(String)  # e.g., "Trade Republic", "Manual", "CSV Import"
    external_id = Column(String)  # ID from external source (e.g., Trade Republic transaction ID)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    portfolio = relationship("Portfolio", back_populates="transactions")
    asset = relationship("Asset", back_populates="transactions")
