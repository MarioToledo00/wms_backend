from django.urls import path
from . import views as viewsAuth
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('request', viewsAuth.request_user),
    path('verify', viewsAuth.verify_email),
    path('checkAuth', TokenVerifyView.as_view(), name='token_verify'),
    path('tokenrefresh', TokenRefreshView.as_view(), name='token_refresh'),
]
