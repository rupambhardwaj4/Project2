from django.urls import path
from .views import invoices

urlpatterns = [
    path("invoices/", invoices, name="invoices"),
]
