# Transaction Analysis Microservice

This project is a REST API microservice for processing and analyzing transactions. It uses FastAPI, Celery, and Redis for asynchronous task processing, and PostgreSQL as the database.

## Features

- **Endpoints:**
  - `POST /transactions` - Upload a transaction.
  - `DELETE /transactions` - Delete all transactions.
  - `GET /statistics` - Retrieve transaction statistics.
- **Asynchronous Processing:**
  - Task queues with Celery and Redis.
- **Database:**
  - Uses PostgreSQL for storing transaction data.
- **Security:**
  - API key authentication.
  - Data validation.
- **Documentation:**
  - Automatically generated Swagger documentation available at `/docs`.

---

## Requirements

- Python 3.8+
- PostgreSQL 12+
- Redis
- Docker (optional for containerized setup)

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/softskate/TestWork545756.git
cd TestWork545756
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and configure the following:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/transactions_db
REDIS_URL=redis://localhost:6379/0
API_KEY=your_api_key
```

### 5. Set Up PostgreSQL Database
Create the database:
```sql
CREATE DATABASE transactions_db;
```
Run the migrations:
```bash
alembic upgrade head
```

### 6. Start Redis Server
If Redis is not running, start it:
```bash
redis-server
```

### 7. Run the Application
Start the FastAPI server:
```bash
uvicorn main:app --reload
```

### 8. Start the Celery Worker
```bash
celery -A celery_app.celery_app worker --loglevel=info
```

---

## Using Docker (Optional)

1. Build and run the application with Docker Compose:

```bash
docker-compose up --build
```

2. Access the API documentation at `http://localhost:8000/docs`.

---

## Endpoints

### POST /transactions
**Request:**
```json
{
  "transaction_id": "123456",
  "user_id": "user_001",
  "amount": 150.50,
  "currency": "USD",
  "timestamp": "2024-12-12T12:00:00"
}
```
**Response:**
```json
{
  "message": "Transaction received",
  "task_id": "abcd1234"
}
```

### DELETE /transactions
**Response:**
```json
{
  "message": "All transactions deleted"
}
```

### GET /statistics
**Response:**
```json
{
  "total_transactions": 25,
  "average_transaction_amount": 180.03,
  "top_transactions": [
    {"transaction_id": "1", "amount": 1000},
    {"transaction_id": "2", "amount": 850},
    {"transaction_id": "3", "amount": 500}
  ]
}
```

---

## Testing

Run tests using `pytest`:
```bash
pytest
```

---

## Notes

- Ensure Redis and PostgreSQL are running before starting the application.
- Use `--pool=solo` if running Celery on Windows.
- API requests must include the `Authorization` header with the API key:
  ```
  Authorization: ApiKey your_api_key
  
