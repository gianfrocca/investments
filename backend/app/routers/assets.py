from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.portfolio import Portfolio
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, Asset as AssetSchema, AssetUpdate, AssetWithStats
from app.utils.auth import get_current_active_user
from app.services.asset_service import calculate_asset_stats

router = APIRouter(prefix="/api/assets", tags=["assets"])


@router.get("/portfolio/{portfolio_id}", response_model=List[AssetWithStats])
def list_portfolio_assets(
    portfolio_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    List all assets in a portfolio
    """
    # Verify portfolio ownership
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )

    assets = db.query(Asset).filter(Asset.portfolio_id == portfolio_id).all()

    # Add stats to each asset
    assets_with_stats = []
    for asset in assets:
        stats = calculate_asset_stats(asset, db)
        asset_dict = AssetSchema.from_orm(asset).dict()
        asset_dict['stats'] = stats
        assets_with_stats.append(asset_dict)

    return assets_with_stats


@router.post("/", response_model=AssetSchema, status_code=status.HTTP_201_CREATED)
def create_asset(
    asset_data: AssetCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new asset in a portfolio
    """
    # Verify portfolio ownership
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == asset_data.portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )

    # Check if asset already exists in portfolio
    existing_asset = db.query(Asset).filter(
        Asset.portfolio_id == asset_data.portfolio_id,
        Asset.symbol == asset_data.symbol
    ).first()

    if existing_asset:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Asset with this symbol already exists in the portfolio"
        )

    new_asset = Asset(**asset_data.dict())
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    return new_asset


@router.get("/{asset_id}", response_model=AssetWithStats)
def get_asset(
    asset_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific asset
    """
    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )

    # Verify ownership through portfolio
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == asset.portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )

    # Add stats
    stats = calculate_asset_stats(asset, db)
    asset_dict = AssetSchema.from_orm(asset).dict()
    asset_dict['stats'] = stats

    return asset_dict


@router.put("/{asset_id}", response_model=AssetSchema)
def update_asset(
    asset_id: int,
    asset_data: AssetUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update an asset
    """
    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )

    # Verify ownership
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == asset.portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )

    # Update fields
    update_data = asset_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(asset, field, value)

    db.commit()
    db.refresh(asset)

    return asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(
    asset_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete an asset
    """
    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )

    # Verify ownership
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == asset.portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found"
        )

    db.delete(asset)
    db.commit()

    return None
