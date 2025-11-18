from sqlalchemy.orm import Session
from app.models.asset import Asset
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import TransactionCreate


def process_transaction(transaction_data: TransactionCreate, asset: Asset, db: Session) -> Transaction:
    """
    Process a transaction and update the asset accordingly
    """
    # Calculate total amount
    total_amount = (transaction_data.quantity * transaction_data.price_per_unit) + transaction_data.fees

    # Create transaction
    new_transaction = Transaction(
        portfolio_id=transaction_data.portfolio_id,
        asset_id=transaction_data.asset_id,
        transaction_type=transaction_data.transaction_type,
        quantity=transaction_data.quantity,
        price_per_unit=transaction_data.price_per_unit,
        total_amount=total_amount,
        fees=transaction_data.fees,
        currency=transaction_data.currency,
        transaction_date=transaction_data.transaction_date,
        notes=transaction_data.notes,
        source=transaction_data.source or "Manual",
        external_id=transaction_data.external_id
    )

    db.add(new_transaction)

    # Update asset based on transaction type
    if transaction_data.transaction_type == TransactionType.BUY:
        # Update quantity
        old_quantity = asset.quantity
        new_quantity = old_quantity + transaction_data.quantity

        # Update average buy price
        if asset.average_buy_price:
            total_cost = (old_quantity * asset.average_buy_price) + (
                transaction_data.quantity * transaction_data.price_per_unit
            )
            asset.average_buy_price = total_cost / new_quantity
        else:
            asset.average_buy_price = transaction_data.price_per_unit

        asset.quantity = new_quantity

    elif transaction_data.transaction_type == TransactionType.SELL:
        # Decrease quantity
        asset.quantity -= transaction_data.quantity
        if asset.quantity < 0:
            asset.quantity = 0

    elif transaction_data.transaction_type in [TransactionType.TRANSFER_IN]:
        asset.quantity += transaction_data.quantity

    elif transaction_data.transaction_type in [TransactionType.TRANSFER_OUT]:
        asset.quantity -= transaction_data.quantity
        if asset.quantity < 0:
            asset.quantity = 0

    # For DIVIDEND and FEE, we don't change the quantity

    db.commit()
    db.refresh(new_transaction)

    return new_transaction
