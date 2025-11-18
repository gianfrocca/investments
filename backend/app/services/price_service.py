from sqlalchemy.orm import Session
from datetime import datetime
import yfinance as yf
from typing import Optional

from app.models.asset import Asset, AssetType
from app.models.price_history import PriceHistory
from app.config import settings


def update_asset_price(asset: Asset, price: float, source: str, db: Session):
    """
    Update the current price of an asset and add to price history
    """
    asset.current_price = price
    asset.last_price_update = datetime.utcnow()

    # Add to price history
    price_record = PriceHistory(
        asset_id=asset.id,
        price=price,
        currency=asset.currency,
        timestamp=datetime.utcnow(),
        source=source
    )

    db.add(price_record)
    db.commit()


def fetch_price_from_api(symbol: str, asset_type: AssetType) -> Optional[float]:
    """
    Fetch current price from external API based on asset type
    """
    try:
        if asset_type in [AssetType.STOCK, AssetType.ETF]:
            # Use Yahoo Finance for stocks and ETFs
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if not data.empty:
                return float(data['Close'].iloc[-1])

        elif asset_type == AssetType.CRYPTO:
            # For crypto, add -USD suffix if not present
            crypto_symbol = symbol if '-USD' in symbol else f"{symbol}-USD"
            ticker = yf.Ticker(crypto_symbol)
            data = ticker.history(period="1d")
            if not data.empty:
                return float(data['Close'].iloc[-1])

        return None

    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return None


def update_all_portfolio_prices(portfolio_id: int, db: Session):
    """
    Update prices for all assets in a portfolio
    """
    assets = db.query(Asset).filter(Asset.portfolio_id == portfolio_id).all()

    updated_count = 0
    for asset in assets:
        price = fetch_price_from_api(asset.symbol, asset.asset_type)
        if price:
            update_asset_price(asset, price, "Yahoo Finance", db)
            updated_count += 1

    return {"updated": updated_count, "total": len(assets)}


def update_all_assets_prices(db: Session):
    """
    Update prices for all assets in the system (scheduled task)
    """
    assets = db.query(Asset).all()

    updated_count = 0
    for asset in assets:
        price = fetch_price_from_api(asset.symbol, asset.asset_type)
        if price:
            update_asset_price(asset, price, "Yahoo Finance (Auto)", db)
            updated_count += 1

    return {"updated": updated_count, "total": len(assets)}
