import asyncio
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from celery.result import AsyncResult
from app.database import SessionLocal
from app.models import Transaction
from app.schemas import TransactionCreate, StatisticsResponse
from app.services import get_statistics, validate_api_key
from app.tasks import update_statistics

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/transactions")
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    authorization: str = Header(...)
):
    validate_api_key(authorization)
    db_transaction = Transaction(**transaction.model_dump())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    task: AsyncResult = update_statistics.apply_async()

    return {
        "message": "Transaction received",
        "task_id": task.id
    }

@router.delete("/transactions")
def delete_transactions(db: Session = Depends(get_db), authorization: str = Header(...)):
    validate_api_key(authorization)
    db.query(Transaction).delete()
    db.commit()
    return {"message": "All transactions deleted"}

@router.get("/statistics", response_model=StatisticsResponse)
def get_stats(db: Session = Depends(get_db), authorization: str = Header(...)):
    validate_api_key(authorization)
    return get_statistics(db)
