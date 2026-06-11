from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("employees/", include("apps.employees.urls")),
    path("payroll/", include("apps.payroll.urls")),
    path("documents/", include("apps.documents.urls")),
    path("api/", include("apps.api.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

