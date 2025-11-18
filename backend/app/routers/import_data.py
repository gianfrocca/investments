from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import csv
import io
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.portfolio import Portfolio
from app.utils.auth import get_current_active_user
from app.services.import_service import import_trade_republic_csv, import_generic_csv

router = APIRouter(prefix="/api/import", tags=["import"])


@router.post("/trade-republic/{portfolio_id}")
async def import_trade_republic(
    portfolio_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Import transactions from Trade Republic CSV export

    Expected CSV format:
    Date, Time, Type, Symbol, ISIN, Quantity, Price, Total, Currency, Notes
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

    # Check file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a CSV file"
        )

    # Read file content
    content = await file.read()
    csv_content = content.decode('utf-8')

    try:
        result = import_trade_republic_csv(csv_content, portfolio_id, db)
        return {
            "message": "Import completed successfully",
            "imported": result['imported'],
            "skipped": result['skipped'],
            "errors": result['errors']
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Import failed: {str(e)}"
        )


@router.post("/generic-csv/{portfolio_id}")
async def import_generic(
    portfolio_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Import transactions from generic CSV format

    Expected columns: date, symbol, name, type, quantity, price, fees, currency
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

    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a CSV file"
        )

    content = await file.read()
    csv_content = content.decode('utf-8')

    try:
        result = import_generic_csv(csv_content, portfolio_id, db)
        return {
            "message": "Import completed successfully",
            "imported": result['imported'],
            "skipped": result['skipped'],
            "errors": result['errors']
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Import failed: {str(e)}"
        )


@router.get("/template/trade-republic")
def download_trade_republic_template():
    """
    Download a CSV template for Trade Republic import
    """
    template = """Date,Time,Type,Symbol,ISIN,Quantity,Price,Total,Currency,Notes
2024-01-15,10:30:00,BUY,AAPL,US0378331005,10,150.50,1505.00,USD,Purchase from Trade Republic
2024-01-20,14:15:00,SELL,AAPL,US0378331005,5,155.00,775.00,USD,Partial sale
2024-02-01,09:00:00,DIVIDEND,AAPL,US0378331005,10,0.24,2.40,USD,Quarterly dividend
"""
    return {"content": template, "filename": "trade_republic_template.csv"}


@router.get("/template/generic")
def download_generic_template():
    """
    Download a generic CSV template
    """
    template = """date,symbol,name,type,quantity,price,fees,currency
2024-01-15,AAPL,Apple Inc.,buy,10,150.50,1.99,USD
2024-01-20,MSFT,Microsoft Corp.,buy,5,380.75,1.99,USD
2024-02-01,AAPL,Apple Inc.,dividend,10,0.24,0,USD
"""
    return {"content": template, "filename": "generic_template.csv"}
