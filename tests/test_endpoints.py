import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import pytest
from fastapi.testclient import TestClient
from httpx import Client
from app.main import app
from app.database import Base, engine, SessionLocal
from app.models import Transaction

# Создаем тестовую базу данных
Base.metadata.create_all(bind=engine)

# client = TestClient(app)
client = Client(base_url='http://127.0.0.1:8000', timeout=5)

API_KEY = "ApiKey my_secure_key"

# Фикстура для работы с тестовой базой данных
@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_post_transaction(db_session):
    """Тестирование добавления транзакции через POST /transactions."""
    payload = {
        "transaction_id": "123456",
        "user_id": "user_001",
        "amount": 150.50,
        "currency": "USD",
        "timestamp": "2024-12-12T12:00:00"
    }

    response = client.post(
        "/transactions",
        json=payload,
        headers={"Authorization": API_KEY},
        timeout=20
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Transaction received"

    # Проверяем, что транзакция добавлена в базу данных
    db_transaction = db_session.query(Transaction).filter_by(transaction_id="123456").first()
    assert db_transaction is not None
    assert db_transaction.amount == 150.50


def test_delete_transactions(db_session):
    """Тестирование удаления всех транзакций через DELETE /transactions."""
    # Добавляем тестовую транзакцию
    db_session.add(Transaction(
        transaction_id="123456",
        user_id="user_001",
        amount=150.50,
        currency="USD",
        timestamp="2024-12-12T12:00:00"
    ))
    db_session.commit()

    response = client.delete(
        "/transactions",
        headers={"Authorization": API_KEY}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "All transactions deleted"

    # Проверяем, что транзакции удалены
    transactions = db_session.query(Transaction).all()
    assert len(transactions) == 0


def test_get_statistics(db_session):
    """Тестирование получения статистики через GET /statistics."""
    # Добавляем несколько тестовых транзакций
    transactions = [
        Transaction(transaction_id="1", user_id="user_001", amount=1000, currency="USD", timestamp="2024-12-12T12:00:00"),
        Transaction(transaction_id="2", user_id="user_002", amount=850, currency="USD", timestamp="2024-12-12T12:10:00"),
        Transaction(transaction_id="3", user_id="user_003", amount=500, currency="USD", timestamp="2024-12-12T12:20:00"),
        Transaction(transaction_id="4", user_id="user_004", amount=100, currency="USD", timestamp="2024-12-12T12:30:00"),
    ]
    db_session.add_all(transactions)
    db_session.commit()

    response = client.get(
        "/statistics",
        headers={"Authorization": API_KEY}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["total_transactions"] == 4
    assert round(data["average_transaction_amount"], 2) == 612.5
    assert len(data["top_transactions"]) == 3
    assert data["top_transactions"][0]["amount"] == 1000
    assert data["top_transactions"][1]["amount"] == 850
    assert data["top_transactions"][2]["amount"] == 500
