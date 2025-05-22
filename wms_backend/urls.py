from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('auth/', include('authservice.urls')),
    path('products/', include('products.urls')),
    path('users/', include('users.urls'))
]
