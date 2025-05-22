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
    

    class Meta:
        db_table = 'products'
        managed = False  

