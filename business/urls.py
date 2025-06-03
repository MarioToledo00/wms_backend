from django.urls import path
from .views import BusinessView

urlpatterns = [
    path('<str:action>/', BusinessView.as_view()),
]
