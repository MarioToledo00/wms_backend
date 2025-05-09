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

def createProducts(request):
    if request.method == 'POST':
        for i in range(10):
            product = Products(
                name=f'NameProduct {i+1}',
                description=f'Producto {i+1}',
                sku=f'SKU{i+1}',
                barcode=f'BARCODE{i+1}',
                unit='kg',
                stock_min=10,
                stock_max=100,
                active=True,
                key_product=f'PROD{i+1}',
                updated_by=1,
                categories_id=1,
                brands_id=1
            )
            product.save()
        return JsonResponse({"message": "10 productos creados exitosamente"}, status=201)
    return JsonResponse({"error": "Método no permitido"}, status=405)