from django.http import JsonResponse
from .models import Products,Brands,Categories,Inventory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import F

from django.utils import timezone 

class ProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, action=None):
        if action == "getAllProducts":
            return self.get_inventory_with_products(request)
        elif action == "getAllBrands":
            return self.getAllBrands(request)
        elif action == "getAllCategories":
            return self.getAllCategories(request)
        else:
            return JsonResponse({'error': 'Acción no válida', "action": action}, status=400)
    
    def post(self, request, action=None):  
            return JsonResponse({'error': 'Acción no válida'}, status=400)
    
    def getAllProducts(self,request):
        if request.method == 'GET':
            products = Products.objects.filter(deleted_at__isnull=True).order_by('name').values('id', 'name', 'description','sku','barcode','unit','stock_min','stock_max','active','key_product','created_at','updated_at','deleted_at','updated_by','category__name','brand__name')
            return JsonResponse(list(products), safe=False)
        
    def get_inventory_with_products(self,request):
        if request.method == 'GET':
            inventory_data = (
                Inventory.objects
                .filter(product__deleted_at__isnull=True)  # solo productos no eliminados
                .annotate(
                    product_name=F('product__name'),
                    category_name=F('product__category__name'),
                    brand_name=F('product__brand__name'),
                    active=F('product__active'),
                    warehouse_name=F('warehouse_location__warehouse__name')
                )
                .values(
                    'product__id',
                    'product_name',
                    'category_name',
                    'brand_name',
                    'active',
                    'location',
                    'stock',
                    'warehouse_name'
                )
                .order_by('product_name')
            )
            return JsonResponse(list(inventory_data), safe=False)
    
    def getAllBrands(self,request):
        if request.method == 'GET':
            brands = Brands.objects.filter(deleted_at__isnull=True).order_by('name').values('id', 'name')
            return JsonResponse(list(brands), safe=False)
    
    def getAllCategories(self,request):
        if request.method == 'GET':
            categories = Categories.objects.filter(deleted_at__isnull=True).order_by('name').values('id', 'name')
            return JsonResponse(list(categories), safe=False)

# from django.shortcuts import render
# from django.http import HttpResponse, JsonResponse
# from .models import Products

# Create your views here.

# def getall(request):
#     AllProducts = list(Products.objects.values())
#     return JsonResponse(AllProducts, safe=False)

# def get(request, id):
#     Product = list(Products.objects.filter(id=id).values())
#     # if not Product:
#     #     return JsonResponse(list({ "error": "Product not found"}), safe=False)
#     return JsonResponse(Product, safe=False)

# def createProducts(request):
#     if request.method == 'POST':
#         for i in range(10):
#             product = Products(
#                 name=f'NameProduct {i+1}',
#                 description=f'Producto {i+1}',
#                 sku=f'SKU{i+1}',
#                 barcode=f'BARCODE{i+1}',
#                 unit='kg',
#                 stock_min=10,
#                 stock_max=100,
#                 active=True,
#                 key_product=f'PROD{i+1}',
#                 updated_by=1,
#                 categories_id=1,
#                 brands_id=1
#             )
#             product.save()
#         return JsonResponse({"message": "10 productos creados exitosamente"}, status=201)
#     return JsonResponse({"error": "Método no permitido"}, status=405)