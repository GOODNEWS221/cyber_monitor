from django.urls import path
from .import views

urlpatterns = [
    path("", views.dashboard, name='dashboard'),

    path('api/logs/', api_views.get_logs, name='api_logs'),
    path('api/alerts/', api_views.get_alerts, name='api_alerts'),
]



