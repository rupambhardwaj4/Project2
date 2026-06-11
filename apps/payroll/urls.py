from django.urls import path
from .views import payroll_dashboard

urlpatterns = [
    path("", payroll_dashboard, name="payroll"),
]
