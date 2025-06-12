from django.db import models

# Create your models here.


class Brands(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    deleted_at = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'brands'
        managed = False  

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    deleted_at = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        managed = False
class Products(models.Model):
    class Unit(models.TextChoices):
        KG = 'kg', 'Kilogramo'
        LITER = 'L', 'Litro'
        PIEZA = 'pza', 'Pieza'
        METRO = 'm', 'Metro'
        CENTIMETRO = 'cm', 'Centímetro'
        GRAMO = 'g', 'Gramo'
        MILILITRO = 'ml', 'Mililitro'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    sku = models.CharField(max_length=50, unique=True)
    barcode = models.CharField(max_length=50, unique=True)
    unit = models.CharField(
        max_length=50,
        choices=Unit.choices,  # Usamos las opciones definidas en la clase Unit
        default=Unit.KG,  # Valor por defecto (puedes cambiarlo según sea necesario)
    )
    stock_min = models.IntegerField()
    stock_max = models.IntegerField()
    active = models.PositiveSmallIntegerField(default=True)
    key_product = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True)
    deleted_at = models.DateField(null=True, blank=True)
    updated_by = models.IntegerField()
    brand = models.ForeignKey(Brands, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        managed = False

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(blank=True, null=True)
    deleted_at = models.DateField(blank=True, null=True)
    updated_by = models.IntegerField()

    class Meta:
        db_table = 'warehouses'

    def __str__(self):
        return self.name


class WarehouseLocation(models.Model):
    address = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(blank=True, null=True)
    deleted_at = models.DateField(blank=True, null=True)
    updated_by = models.IntegerField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='locations',db_column='warehouses_id')

    class Meta:
        db_table = 'warehouse_locations'

    def __str__(self):
        return self.address


class Inventory(models.Model):
    location = models.CharField(max_length=70, unique=True)
    stock = models.IntegerField(default=0)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='inventories',db_column='products_id')
    warehouse_location = models.ForeignKey(WarehouseLocation, on_delete=models.CASCADE, related_name='inventories', db_column='warehouse_locations_id')

    class Meta:
        db_table = 'inventory'
        unique_together = ('product', 'warehouse_location')
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventories'

    def __str__(self):
        return f'{self.location} - {self.product.name} - Stock: {self.stock}'
