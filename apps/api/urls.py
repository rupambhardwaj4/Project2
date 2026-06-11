from django.urls import path

try:
    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
except Exception:
    TokenObtainPairView = None
    TokenRefreshView = None

urlpatterns = [
]

if TokenObtainPairView and TokenRefreshView:
    urlpatterns += [
        path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    ]
