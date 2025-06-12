from django.urls import path
from .views import CountView

urlpatterns = [
    path('<str:action>/', CountView.as_view()),
]
