from django.urls import path
from . import views as viewsAuth

urlpatterns = [
    path('login', viewsAuth.login),
    path('logout', viewsAuth.logout),
    path('request', viewsAuth.request_user),
]
