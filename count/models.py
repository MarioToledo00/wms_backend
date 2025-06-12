from django.db import models
from products.models import Products, Brands, Categories
from users.models import Users

# Create your models here.
class Warehouses(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=99)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True)
    deleted_at = models.DateField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'warehouses'
        managed = False

class WarehouseLocations(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=99)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True)
    deleted_at = models.DateField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    warehouses = models.ForeignKey(Warehouses, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.address

    class Meta:
        db_table = 'warehouse_locations'
        managed = False

class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=25)
    stock = models.IntegerField()
    products = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    warehouse_locations = models.ForeignKey(WarehouseLocations, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'inventory'
        managed = False

class InventoryCount(models.Model):
    id = models.AutoField(primary_key=True)
    warehouse_locations = models.ForeignKey(WarehouseLocations, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=25)
    counts = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    canceled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'inventory_count'
        managed = False

class ProductCount(models.Model):
    id = models.AutoField(primary_key=True)
    inventory_count = models.ForeignKey(InventoryCount, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    final_quantity = models.IntegerField()
    first_quantity = models.IntegerField()
    second_quantity = models.IntegerField()
    counted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'product_count'
        managed = False





