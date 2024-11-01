from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from ..views.views_v1 import LoginViewSet, LogoutViewSet

urlpatterns = [
    # --------------------------- JWT Token ------------------------ #
    path("token/refresh/", TokenRefreshView.as_view()),
    path("token/verify/", TokenVerifyView.as_view()),
    # --------------------------- Login & Logout ------------------------ #
    path("login/", LoginViewSet.as_view({"post": "create"}), name="login"),
    path("logout/", LogoutViewSet.as_view({"post": "create"}), name="logout"),
]
