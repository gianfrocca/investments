from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User
from app.models.asset import Asset
from app.models.price_history import PriceHistory
from app.schemas.price import PriceUpdate, PriceHistoryResponse
from app.utils.auth import get_current_active_user
from app.services.price_service import update_asset_price, update_all_portfolio_prices

router = APIRouter(prefix="/api/prices", tags=["prices"])


@router.post("/update/{asset_id}")
def update_price(
    asset_id: int,
    price_data: PriceUpdate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Manually update price for an asset
    """
    asset = db.query(Asset).join(Portfolio).filter(
        Asset.id == asset_id,
        Portfolio.user_id == current_user.id
    ).first()

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )

    # Update price
    update_asset_price(asset, price_data.price, price_data.source, db)

    return {"message": "Price updated successfully", "new_price": price_data.price}


@router.post("/update-portfolio/{portfolio_id}")
def update_portfolio_prices(
    portfolio_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update prices for all assets in a portfolio using external API
    """
    from app.models.portfolio import Portfolio

    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )

    # Update prices in background
    background_tasks.add_task(update_all_portfolio_prices, portfolio_id, db)

    return {"message": "Price update started for all assets"}


@router.get("/history/{asset_id}", response_model=PriceHistoryResponse)
def get_price_history(
    asset_id: int,
    days: int = 30,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get price history for an asset
    """
    from app.models.portfolio import Portfolio

    asset = db.query(Asset).join(Portfolio).filter(
        Asset.id == asset_id,
        Portfolio.user_id == current_user.id
    ).first()

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )

    # Get history
    start_date = datetime.utcnow() - timedelta(days=days)
    history = db.query(PriceHistory).filter(
        PriceHistory.asset_id == asset_id,
        PriceHistory.timestamp >= start_date
    ).order_by(PriceHistory.timestamp.asc()).all()

    return {
        "asset_id": asset_id,
        "symbol": asset.symbol,
        "history": [
            {
                "timestamp": h.timestamp,
                "price": h.price,
                "source": h.source
            }
            for h in history
        ]
    }
