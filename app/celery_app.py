from celery import Celery

# Настройка Celery
celery_app = Celery(
    "app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)
celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.timezone = "UTC"
celery_app.autodiscover_tasks(["app.tasks"])
