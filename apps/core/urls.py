from django.urls import path
from .views import landing, dashboard, salary_slip, settings_page

urlpatterns = [
    path("", landing, name="landing"),
    path("dashboard/", dashboard, name="dashboard"),
    path("settings/", settings_page, name="settings"),
    path("salary-slip/", salary_slip, name="salaryslip"),
]
