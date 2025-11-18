from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreate, Portfolio as PortfolioSchema, PortfolioUpdate, PortfolioWithStats
from app.utils.auth import get_current_active_user
from app.services.portfolio_service import calculate_portfolio_stats

router = APIRouter(prefix="/api/portfolios", tags=["portfolios"])


@router.get("/", response_model=List[PortfolioWithStats])
def list_portfolios(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    List all portfolios for the current user
    """
    portfolios = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).all()

    # Add stats to each portfolio
    portfolios_with_stats = []
    for portfolio in portfolios:
        stats = calculate_portfolio_stats(portfolio, db)
        portfolio_dict = PortfolioSchema.from_orm(portfolio).dict()
        portfolio_dict['stats'] = stats
        portfolios_with_stats.append(portfolio_dict)

    return portfolios_with_stats


@router.post("/", response_model=PortfolioSchema, status_code=status.HTTP_201_CREATED)
def create_portfolio(
    portfolio_data: PortfolioCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new portfolio
    """
    new_portfolio = Portfolio(
        name=portfolio_data.name,
        description=portfolio_data.description,
        user_id=current_user.id
    )

    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)

    return new_portfolio


@router.get("/{portfolio_id}", response_model=PortfolioWithStats)
def get_portfolio(
    portfolio_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific portfolio
    """
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )

    # Add stats
    stats = calculate_portfolio_stats(portfolio, db)
    portfolio_dict = PortfolioSchema.from_orm(portfolio).dict()
    portfolio_dict['stats'] = stats

    return portfolio_dict


@router.put("/{portfolio_id}", response_model=PortfolioSchema)
def update_portfolio(
    portfolio_id: int,
    portfolio_data: PortfolioUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a portfolio
    """
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )

    # Update fields
    if portfolio_data.name is not None:
        portfolio.name = portfolio_data.name
    if portfolio_data.description is not None:
        portfolio.description = portfolio_data.description

    db.commit()
    db.refresh(portfolio)

    return portfolio


@router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_portfolio(
    portfolio_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a portfolio
    """
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )

    db.delete(portfolio)
    db.commit()

    return None
