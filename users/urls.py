from django.urls import path
from .views import UserView

urlpatterns = [
    path('<str:action>/', UserView.as_view()),
]
