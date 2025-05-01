from django.db import models

# Create your models here.

class Products(models.Model):
    id = models.AutoField(primary_key=True)
    cve_producto = models.CharField(max_length=100)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=50)
    lin = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    com_icms = models.DecimalField(max_digits=10, decimal_places=2)
    reserva = models.IntegerField()
    reserva2 = models.IntegerField()
    disponible = models.IntegerField()
    st = models.CharField(max_length=50)
    krdx = models.IntegerField()
    det = models.IntegerField()

    class Meta:
        db_table = 'products'
        managed = False  # Para que Django no intente crear/modificar la tabla