from django.urls import path
from .views import directory

urlpatterns = [
    path("", directory, name="directory"),
]
