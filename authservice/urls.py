from django.urls import path
from . import views as viewsAuth

urlpatterns = [
    path('login', viewsAuth.login),
    path('logout', viewsAuth.logout),
    path('request', viewsAuth.request_user),
    path('verify', viewsAuth.verify_email),
    path('create_user_post', viewsAuth.create_user_by_post),
    path('checkAuth', viewsAuth.check_Auth),
]
