import csv
import io
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Dict, List

from app.models.asset import Asset, AssetType
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import TransactionCreate
from app.services.transaction_service import process_transaction


def parse_trade_republic_date(date_str: str, time_str: str = "") -> datetime:
    """
    Parse Trade Republic date/time format
    """
    try:
        if time_str:
            dt_str = f"{date_str} {time_str}"
            return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        else:
            return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        # Try alternative formats
        try:
            return datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            return datetime.now()


def determine_asset_type(symbol: str, isin: str = "") -> AssetType:
    """
    Determine asset type from symbol or ISIN
    """
    # Crypto patterns
    crypto_symbols = ['BTC', 'ETH', 'ADA', 'DOT', 'SOL', 'MATIC', 'AVAX']
    if any(crypto in symbol.upper() for crypto in crypto_symbols):
        return AssetType.CRYPTO

    # ETF patterns (common ISIN prefixes)
    if isin and (isin.startswith('IE') or 'ETF' in symbol.upper()):
        return AssetType.ETF

    # Default to stock
    return AssetType.STOCK


def import_trade_republic_csv(csv_content: str, portfolio_id: int, db: Session) -> Dict:
    """
    Import transactions from Trade Republic CSV export

    Expected format:
    Date,Time,Type,Symbol,ISIN,Quantity,Price,Total,Currency,Notes
    """
    csv_file = io.StringIO(csv_content)
    reader = csv.DictReader(csv_file)

    imported = 0
    skipped = 0
    errors = []

    for row_num, row in enumerate(reader, start=2):
        try:
            # Parse data
            date_str = row.get('Date', '').strip()
            time_str = row.get('Time', '').strip()
            trans_type = row.get('Type', '').strip().upper()
            symbol = row.get('Symbol', '').strip()
            isin = row.get('ISIN', '').strip()
            quantity = float(row.get('Quantity', 0))
            price = float(row.get('Price', 0))
            total = float(row.get('Total', 0))
            currency = row.get('Currency', 'EUR').strip()
            notes = row.get('Notes', '').strip()

            if not symbol or quantity <= 0 or price <= 0:
                skipped += 1
                continue

            # Determine transaction type
            transaction_type = TransactionType.BUY
            if trans_type in ['SELL', 'SALE']:
                transaction_type = TransactionType.SELL
            elif trans_type in ['DIVIDEND', 'DIV']:
                transaction_type = TransactionType.DIVIDEND

            # Get or create asset
            asset = db.query(Asset).filter(
                Asset.portfolio_id == portfolio_id,
                Asset.symbol == symbol
            ).first()

            if not asset:
                # Create new asset
                asset_type = determine_asset_type(symbol, isin)
                asset = Asset(
                    portfolio_id=portfolio_id,
                    symbol=symbol,
                    name=symbol,  # Will be updated later
                    asset_type=asset_type,
                    isin=isin,
                    quantity=0,
                    currency=currency
                )
                db.add(asset)
                db.commit()
                db.refresh(asset)

            # Check if transaction already exists (avoid duplicates)
            external_id = f"TR_{date_str}_{symbol}_{quantity}_{price}"
            existing = db.query(Transaction).filter(
                Transaction.external_id == external_id
            ).first()

            if existing:
                skipped += 1
                continue

            # Create transaction
            transaction_date = parse_trade_republic_date(date_str, time_str)

            transaction_data = TransactionCreate(
                portfolio_id=portfolio_id,
                asset_id=asset.id,
                transaction_type=transaction_type,
                quantity=quantity,
                price_per_unit=price,
                fees=0.0,  # Trade Republic often includes fees in the total
                currency=currency,
                transaction_date=transaction_date,
                notes=notes,
                source="Trade Republic",
                external_id=external_id
            )

            process_transaction(transaction_data, asset, db)
            imported += 1

        except Exception as e:
            errors.append(f"Row {row_num}: {str(e)}")
            continue

    return {
        "imported": imported,
        "skipped": skipped,
        "errors": errors
    }


def import_generic_csv(csv_content: str, portfolio_id: int, db: Session) -> Dict:
    """
    Import transactions from generic CSV format

    Expected columns: date, symbol, name, type, quantity, price, fees, currency
    """
    csv_file = io.StringIO(csv_content)
    reader = csv.DictReader(csv_file)

    imported = 0
    skipped = 0
    errors = []

    for row_num, row in enumerate(reader, start=2):
        try:
            # Parse data
            date_str = row.get('date', '').strip()
            symbol = row.get('symbol', '').strip()
            name = row.get('name', symbol).strip()
            trans_type = row.get('type', 'buy').strip().lower()
            quantity = float(row.get('quantity', 0))
            price = float(row.get('price', 0))
            fees = float(row.get('fees', 0))
            currency = row.get('currency', 'EUR').strip()

            if not symbol or quantity <= 0 or price <= 0:
                skipped += 1
                continue

            # Map transaction type
            type_mapping = {
                'buy': TransactionType.BUY,
                'sell': TransactionType.SELL,
                'dividend': TransactionType.DIVIDEND,
                'fee': TransactionType.FEE,
            }
            transaction_type = type_mapping.get(trans_type, TransactionType.BUY)

            # Get or create asset
            asset = db.query(Asset).filter(
                Asset.portfolio_id == portfolio_id,
                Asset.symbol == symbol
            ).first()

            if not asset:
                asset_type = determine_asset_type(symbol)
                asset = Asset(
                    portfolio_id=portfolio_id,
                    symbol=symbol,
                    name=name,
                    asset_type=asset_type,
                    quantity=0,
                    currency=currency
                )
                db.add(asset)
                db.commit()
                db.refresh(asset)

            # Create transaction
            transaction_date = datetime.strptime(date_str, "%Y-%m-%d")

            transaction_data = TransactionCreate(
                portfolio_id=portfolio_id,
                asset_id=asset.id,
                transaction_type=transaction_type,
                quantity=quantity,
                price_per_unit=price,
                fees=fees,
                currency=currency,
                transaction_date=transaction_date,
                source="CSV Import"
            )

            process_transaction(transaction_data, asset, db)
            imported += 1

        except Exception as e:
            errors.append(f"Row {row_num}: {str(e)}")
            continue

    return {
        "imported": imported,
        "skipped": skipped,
        "errors": errors
    }
