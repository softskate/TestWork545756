from app.celery_app import celery_app
from sqlalchemy import func
from app.database import SessionLocal
from app.models import Transaction

@celery_app.task
def update_statistics():
    """Обновляет статистику по транзакциям."""
    db = SessionLocal()
    try:
        # Пример простой обработки статистики
        total_transactions = db.query(Transaction).count()
        avg_amount = db.query(Transaction).with_entities(func.avg(Transaction.amount)).scalar() or 0
        top_transactions = (
            db.query(Transaction)
            .order_by(Transaction.amount.desc())
            .limit(3)
            .all()
        )

        # Логируем статистику
        print("Общее количество транзакций:", total_transactions)
        print("Средняя сумма транзакций:", avg_amount)
        print("Топ-3 транзакции:", [t.amount for t in top_transactions])
    finally:
        db.close()
