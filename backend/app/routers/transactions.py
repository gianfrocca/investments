from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.portfolio import Portfolio
from app.models.asset import Asset
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, Transaction as TransactionSchema, TransactionWithAsset
from app.utils.auth import get_current_active_user
from app.services.transaction_service import process_transaction

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.get("/portfolio/{portfolio_id}", response_model=List[TransactionWithAsset])
def list_portfolio_transactions(
    portfolio_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    limit: int = 100,
    offset: int = 0
):
    """
    List transactions for a portfolio
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

    transactions = db.query(Transaction, Asset.symbol, Asset.name).join(
        Asset, Transaction.asset_id == Asset.id
    ).filter(
        Transaction.portfolio_id == portfolio_id
    ).order_by(
        Transaction.transaction_date.desc()
    ).limit(limit).offset(offset).all()

    # Format response
    result = []
    for transaction, symbol, name in transactions:
        trans_dict = TransactionSchema.from_orm(transaction).dict()
        trans_dict['asset_symbol'] = symbol
        trans_dict['asset_name'] = name
        result.append(trans_dict)

    return result


@router.get("/asset/{asset_id}", response_model=List[TransactionSchema])
def list_asset_transactions(
    asset_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    List transactions for a specific asset
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

    transactions = db.query(Transaction).filter(
        Transaction.asset_id == asset_id
    ).order_by(Transaction.transaction_date.desc()).all()

    return transactions


@router.post("/", response_model=TransactionSchema, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new transaction
    """
    # Verify portfolio ownership
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == transaction_data.portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )

    # Verify asset exists and belongs to portfolio
    asset = db.query(Asset).filter(
        Asset.id == transaction_data.asset_id,
        Asset.portfolio_id == transaction_data.portfolio_id
    ).first()

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found in this portfolio"
        )

    # Process transaction (updates asset quantity and average price)
    new_transaction = process_transaction(transaction_data, asset, db)

    return new_transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a transaction (Note: This will not automatically recalculate asset quantities)
    """
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    # Verify ownership
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == transaction.portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    db.delete(transaction)
    db.commit()

    return None
