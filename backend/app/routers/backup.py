from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime
import json
import io

from app.database import get_db
from app.models.user import User
from app.utils.auth import get_current_active_user
from app.services.backup_service import export_user_data, export_portfolio_data, import_user_data

router = APIRouter(prefix="/api/backup", tags=["backup"])


@router.get("/export/all")
def export_all_data(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Export all user data as JSON
    """
    data = export_user_data(current_user.id, db)

    # Create JSON file
    json_str = json.dumps(data, indent=2, default=str)
    filename = f"investment_backup_{current_user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    return StreamingResponse(
        io.BytesIO(json_str.encode()),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/export/portfolio/{portfolio_id}")
def export_portfolio(
    portfolio_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Export a single portfolio as JSON
    """
    from app.models.portfolio import Portfolio

    # Verify ownership
    portfolio = db.query(Portfolio).filter(
        Portfolio.id == portfolio_id,
        Portfolio.user_id == current_user.id
    ).first()

    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )

    data = export_portfolio_data(portfolio_id, db)

    json_str = json.dumps(data, indent=2, default=str)
    filename = f"portfolio_{portfolio.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    return StreamingResponse(
        io.BytesIO(json_str.encode()),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.post("/import")
async def import_backup(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Import user data from JSON backup file
    """
    if not file.filename.endswith('.json'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a JSON file"
        )

    content = await file.read()

    try:
        data = json.loads(content.decode('utf-8'))
        result = import_user_data(data, current_user.id, db)

        return {
            "message": "Import completed successfully",
            "portfolios_imported": result['portfolios_imported'],
            "assets_imported": result['assets_imported'],
            "transactions_imported": result['transactions_imported']
        }
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON file"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Import failed: {str(e)}"
        )
