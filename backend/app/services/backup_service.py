from sqlalchemy.orm import Session
from typing import Dict, List
from datetime import datetime

from app.models.portfolio import Portfolio
from app.models.asset import Asset
from app.models.transaction import Transaction
from app.models.price_history import PriceHistory


def export_user_data(user_id: int, db: Session) -> Dict:
    """
    Export all data for a user as a JSON-serializable dictionary
    """
    portfolios = db.query(Portfolio).filter(Portfolio.user_id == user_id).all()

    export_data = {
        "export_date": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "portfolios": []
    }

    for portfolio in portfolios:
        portfolio_data = export_portfolio_data(portfolio.id, db)
        export_data["portfolios"].append(portfolio_data)

    return export_data


def export_portfolio_data(portfolio_id: int, db: Session) -> Dict:
    """
    Export a single portfolio with all its data
    """
    portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()

    if not portfolio:
        return {}

    assets = db.query(Asset).filter(Asset.portfolio_id == portfolio_id).all()

    portfolio_data = {
        "id": portfolio.id,
        "name": portfolio.name,
        "description": portfolio.description,
        "created_at": portfolio.created_at.isoformat() if portfolio.created_at else None,
        "assets": []
    }

    for asset in assets:
        # Get transactions for this asset
        transactions = db.query(Transaction).filter(
            Transaction.asset_id == asset.id
        ).order_by(Transaction.transaction_date).all()

        # Get price history
        price_history = db.query(PriceHistory).filter(
            PriceHistory.asset_id == asset.id
        ).order_by(PriceHistory.timestamp.desc()).limit(100).all()

        asset_data = {
            "symbol": asset.symbol,
            "name": asset.name,
            "asset_type": asset.asset_type.value,
            "isin": asset.isin,
            "quantity": asset.quantity,
            "average_buy_price": asset.average_buy_price,
            "current_price": asset.current_price,
            "currency": asset.currency,
            "transactions": [
                {
                    "transaction_type": t.transaction_type.value,
                    "quantity": t.quantity,
                    "price_per_unit": t.price_per_unit,
                    "total_amount": t.total_amount,
                    "fees": t.fees,
                    "currency": t.currency,
                    "transaction_date": t.transaction_date.isoformat(),
                    "notes": t.notes,
                    "source": t.source,
                    "external_id": t.external_id
                }
                for t in transactions
            ],
            "price_history": [
                {
                    "timestamp": ph.timestamp.isoformat(),
                    "price": ph.price,
                    "source": ph.source
                }
                for ph in price_history
            ]
        }

        portfolio_data["assets"].append(asset_data)

    return portfolio_data


def import_user_data(data: Dict, user_id: int, db: Session) -> Dict:
    """
    Import user data from a backup file
    """
    portfolios_imported = 0
    assets_imported = 0
    transactions_imported = 0

    for portfolio_data in data.get("portfolios", []):
        # Create portfolio
        portfolio = Portfolio(
            user_id=user_id,
            name=portfolio_data.get("name", "Imported Portfolio"),
            description=portfolio_data.get("description")
        )
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
        portfolios_imported += 1

        # Import assets and transactions
        for asset_data in portfolio_data.get("assets", []):
            # Create asset
            from app.models.asset import AssetType
            asset = Asset(
                portfolio_id=portfolio.id,
                symbol=asset_data["symbol"],
                name=asset_data["name"],
                asset_type=AssetType(asset_data["asset_type"]),
                isin=asset_data.get("isin"),
                quantity=asset_data.get("quantity", 0),
                average_buy_price=asset_data.get("average_buy_price"),
                current_price=asset_data.get("current_price"),
                currency=asset_data.get("currency", "EUR")
            )
            db.add(asset)
            db.commit()
            db.refresh(asset)
            assets_imported += 1

            # Import transactions
            from app.models.transaction import TransactionType
            for trans_data in asset_data.get("transactions", []):
                transaction = Transaction(
                    portfolio_id=portfolio.id,
                    asset_id=asset.id,
                    transaction_type=TransactionType(trans_data["transaction_type"]),
                    quantity=trans_data["quantity"],
                    price_per_unit=trans_data["price_per_unit"],
                    total_amount=trans_data["total_amount"],
                    fees=trans_data.get("fees", 0),
                    currency=trans_data.get("currency", "EUR"),
                    transaction_date=datetime.fromisoformat(trans_data["transaction_date"]),
                    notes=trans_data.get("notes"),
                    source=trans_data.get("source", "Import"),
                    external_id=trans_data.get("external_id")
                )
                db.add(transaction)
                transactions_imported += 1

            # Import price history (optional)
            for price_data in asset_data.get("price_history", []):
                price_record = PriceHistory(
                    asset_id=asset.id,
                    price=price_data["price"],
                    timestamp=datetime.fromisoformat(price_data["timestamp"]),
                    source=price_data.get("source", "Import")
                )
                db.add(price_record)

            db.commit()

    return {
        "portfolios_imported": portfolios_imported,
        "assets_imported": assets_imported,
        "transactions_imported": transactions_imported
    }
