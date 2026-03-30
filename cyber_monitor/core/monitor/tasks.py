from celery import shared_task
from .ml_model import train_model
from .models import Company


@shared_task
def retrain_ml_models():
    """
    Retrain ML models for all companies periodically
    """
    companies = Company.objects.all()
    for company in companies:
        train_model(company)
    return f"Retrained ML models for {companies.count()} companies "