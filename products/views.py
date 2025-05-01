from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Products

# Create your views here.

def getall(request):
    AllProducts = list(Products.objects.values())
    return JsonResponse(AllProducts, safe=False)

def get(request, id):
    Product = list(Products.objects.filter(id=id).values())
    # if not Product:
    #     return JsonResponse(list({ "error": "Product not found"}), safe=False)
    return JsonResponse(Product, safe=False)