# from django.urls import path
# from . import views as viewsProducts

# urlpatterns = [
#     path('getall', viewsProducts.getall),
#     path('get/<int:id>', viewsProducts.get),
#     path('createProducts', viewsProducts.createProducts)
# ]
from django.urls import path
from .views import ProductsView

urlpatterns = [
    path('<str:action>/', ProductsView.as_view()),
]
