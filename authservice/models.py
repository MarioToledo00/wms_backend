from django.db import models

# Create your models here.

class Users(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    empleado_id = models.IntegerField(max_length=10)
    usuario_alta = models.IntegerField(max_length=10)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    usuario_modif = models.IntegerField(null=True, blank=True)
    fecha_modif = models.DateTimeField(null=True, blank=True)
    usuario_baja = models.IntegerField( null=True, blank=True)
    fecha_baja = models.DateTimeField(null=True, blank=True)

