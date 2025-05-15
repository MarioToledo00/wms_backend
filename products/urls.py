from django.urls import path
from . import views as viewsProducts

urlpatterns = [
    path('getall', viewsProducts.getall),
    path('get/<int:id>', viewsProducts.get),
    path('createProducts', viewsProducts.createProducts)
]