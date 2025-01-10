from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Transaction
from sqlalchemy import func

def get_statistics(db: Session):
    total_transactions = db.query(Transaction).count()
    if total_transactions == 0:
        return {"total_transactions": 0, "average_transaction_amount": 0, "top_transactions": []}

    avg_amount = db.query(func.avg(Transaction.amount)).scalar()
    top_transactions = (
        db.query(Transaction)
        .order_by(Transaction.amount.desc())
        .limit(3)
        .all()
    )
    return {
        "total_transactions": total_transactions,
        "average_transaction_amount": avg_amount,
        "top_transactions": [
            {"transaction_id": t.transaction_id, "amount": t.amount} for t in top_transactions
        ],
    }

def validate_api_key(api_key: str):
    expected_key = "ApiKey my_secure_key"
    if api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
