from sqlalchemy.orm import Session
from app.models.portfolio import Portfolio
from app.models.asset import Asset
from app.models.transaction import Transaction, TransactionType


def calculate_portfolio_stats(portfolio: Portfolio, db: Session) -> dict:
    """
    Calculate statistics for a portfolio
    """
    assets = db.query(Asset).filter(Asset.portfolio_id == portfolio.id).all()

    total_value = 0.0
    total_invested = 0.0

    for asset in assets:
        if asset.current_price and asset.quantity:
            total_value += asset.current_price * asset.quantity

        if asset.average_buy_price and asset.quantity:
            total_invested += asset.average_buy_price * asset.quantity

    total_gain_loss = total_value - total_invested
    total_gain_loss_percentage = (
        (total_gain_loss / total_invested * 100) if total_invested > 0 else 0.0
    )

    return {
        "total_value": round(total_value, 2),
        "total_invested": round(total_invested, 2),
        "total_gain_loss": round(total_gain_loss, 2),
        "total_gain_loss_percentage": round(total_gain_loss_percentage, 2),
        "asset_count": len(assets)
    }
