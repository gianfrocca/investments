from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.asset import Asset
from app.models.transaction import Transaction, TransactionType


def calculate_asset_stats(asset: Asset, db: Session) -> dict:
    """
    Calculate statistics for an asset
    """
    # Calculate total invested from buy transactions
    total_invested = 0.0
    if asset.average_buy_price and asset.quantity:
        total_invested = asset.average_buy_price * asset.quantity

    # Calculate current value
    current_value = 0.0
    if asset.current_price and asset.quantity:
        current_value = asset.current_price * asset.quantity

    # Calculate gain/loss
    gain_loss = current_value - total_invested
    gain_loss_percentage = (
        (gain_loss / total_invested * 100) if total_invested > 0 else 0.0
    )

    # Calculate total dividends
    total_dividends = db.query(
        func.sum(Transaction.total_amount)
    ).filter(
        Transaction.asset_id == asset.id,
        Transaction.transaction_type == TransactionType.DIVIDEND
    ).scalar() or 0.0

    return {
        "total_invested": round(total_invested, 2),
        "current_value": round(current_value, 2),
        "gain_loss": round(gain_loss, 2),
        "gain_loss_percentage": round(gain_loss_percentage, 2),
        "total_dividends": round(total_dividends, 2)
    }


def recalculate_asset_average_price(asset: Asset, db: Session):
    """
    Recalculate the average buy price for an asset based on all buy transactions
    """
    buy_transactions = db.query(Transaction).filter(
        Transaction.asset_id == asset.id,
        Transaction.transaction_type == TransactionType.BUY
    ).all()

    if not buy_transactions:
        asset.average_buy_price = 0.0
        asset.quantity = 0.0
        return

    total_cost = sum(t.total_amount for t in buy_transactions)
    total_quantity = sum(t.quantity for t in buy_transactions)

    # Subtract sold quantities
    sell_transactions = db.query(Transaction).filter(
        Transaction.asset_id == asset.id,
        Transaction.transaction_type == TransactionType.SELL
    ).all()

    total_sold = sum(t.quantity for t in sell_transactions)

    asset.quantity = total_quantity - total_sold
    asset.average_buy_price = total_cost / total_quantity if total_quantity > 0 else 0.0

    db.commit()
