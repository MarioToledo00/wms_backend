from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import F,Q
from .models import InventoryCount, Inventory, WarehouseLocations, Warehouses, ProductCount
from products.models import Products, Brands, Categories
from users.models import Users
import json

from django.utils import timezone 

class CountView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, action=None):
        if action == "getCountsClosed":
            return self.getCountsClosed(request)
        elif action == "getCountsOpen":
            return self.getCountsOpen(request)
        elif action == "warehouseEnable":
            return self.warehouseEnable(request)
        else:
            return JsonResponse({'error': 'Acción no válida', "action": action}, status=400)
    
    def post(self, request, action=None):  
        if action == "create":
            return self.create(request)
        else:
            return JsonResponse({'error': 'Acción no válida'}, status=400)
    
    def getCountsClosed(self, request):
        if request.method == 'GET':
            try:
                inventoryCount = InventoryCount.objects.filter(
                    Q(closed_at__isnull=False) | Q(canceled_at__isnull=False)).values() # type: ignore
                return JsonResponse(list(inventoryCount), safe=False)

            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': 'Error al autenticar',
                    'error': str(e)
                }, status=500)

    def getCountsOpen(self,request):
         if request.method == 'GET':

            try:
                inventoryCount = InventoryCount.objects.filter(
                    Q(closed_at__isnull=True) & Q(canceled_at__isnull=True) ).values('id', 'warehouse_locations__warehouses__name', 'warehouse_locations__address', 'type', 'warehouse_locations__warehouses__id', 'counts', 'created_at') # type: ignore

                inventaryOpens = []

                for inventory in inventoryCount:
                
                    productCount = ProductCount.objects.filter(inventory_count=inventory['id']).values('id', 'product__id', 'product__name', 'counted')

                    total = productCount.count()

                    contados = 0

                    for count in productCount:
                        if count.get('counted'):
                            contados += 1

                    progreso = round((contados / total) * 100) if total > 0 else 0

                    status = 'Abierto' if inventory.get('closed_at') is None else 'Cerrado'
                    if inventory.get('canceled_at') is not None:
                        status = 'Cancelado'

                    data ={
                        'id': inventory.get('id'),
                        'name': inventory.get('warehouse_locations__warehouses__name'),
                        'address': inventory.get('warehouse_locations__address'),
                        'type': inventory.get('type'),
                        'warehouse': inventory.get('warehouse_locations__warehouses__id'),
                        'countType': inventory.get('counts'),
                        'date': inventory.get('created_at'),
                        'status': status,
                        'info': f'Conteos: {inventory.get("counts")} - Productos: {total} - Progreso: {progreso}%',
                        'progress': progreso,
                        'inventory': inventory
                    }

                    inventaryOpens.append(data)
                return JsonResponse(inventaryOpens, safe=False)
  
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': 'Error al autenticar',
                    'error': str(e)
                }, status=500)
                
    def warehouseEnable(self,request):
        if request.method == 'GET':
            try:
                warehouseEnable = WarehouseLocations.objects.exclude(
                                                Q(inventorycount__canceled_at__isnull=False) | 
                                                Q(inventorycount__closed_at__isnull=False)
                                            ).distinct().values('id','address','warehouses__name')
                return JsonResponse(list(warehouseEnable), safe=False)
            
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': 'Error al autenticar',
                    'error': str(e)
                }, status=500)

    def create(self, request):
        if request.method == 'POST':
            
            try:
                data = json.loads(request.body)

                warehouse_location = WarehouseLocations.objects.get(id=data.get('id')) 

                inventory = InventoryCount.objects.create(
                    warehouse_locations=warehouse_location,
                    created_at=timezone.now(),
                    type=data.get('type'),
                    counts=data.get('countType', 1),  # Default to 0 if not provided
                )
                inventory.save()

                products_in_inventory = Inventory.objects.filter(warehouse_locations=warehouse_location['id'])
                for product in products_in_inventory:

                    producto = Products.objects.filter(id=product.products.id).first()
                    
                    try:
                        product_count = ProductCount.objects.create(
                            inventory_count=inventory,
                            product=producto,
                            first_quantity=product.stock
                        )
                    except Exception as e:
                        return JsonResponse({
                            'success': False,
                            'message': 'Error al crear el conteo del producto',
                            'error': str(e)
                        }, status=500)

                    try:
                        product_count.save()
                    except Exception as e:
                        return JsonResponse({
                            'success': False,
                            'message': 'Error al guardar el conteo del producto',
                            'error': str(e)
                        }, status=500)

                return JsonResponse({'success':True,'message': 'Inventario creado correctamente'}, status=201)
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': 'Error al crear el inventario',
                    'error': str(e)
                }, status=500)