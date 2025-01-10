from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    transaction_id: str
    user_id: str
    amount: float
    currency: str
    timestamp: datetime

class StatisticsResponse(BaseModel):
    total_transactions: int
    average_transaction_amount: float
    top_transactions: list[dict]
