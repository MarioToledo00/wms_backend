from django.urls import path
from . import views as viewsAuth

urlpatterns = [
    path('getRequests', viewsAuth.all_request_user),
    path('getRoles', viewsAuth.getRoles),
    path('create_user_post', viewsAuth.create_user_by_post),
    path('create', viewsAuth.create_user)

]
