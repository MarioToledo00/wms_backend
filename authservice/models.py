from django.db import models

# Create your models here.

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    tel = models.CharField(max_length=10)
    rol_id = models.IntegerField(null=True, blank=True)
    password = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True)
    deleted_at = models.DateField(null=True, blank=True)
    activated_by = models.IntegerField()
    class Meta:
        db_table = 'users'

class RequestUser(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    tel = models.CharField(max_length=10)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True)
    verified = models.DateField(null=True, blank=True)
    accepted = models.DateField( null=True, blank=True)
    denied = models.DateField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'request_user'

class EmailVerified(models.Model):
    token = models.CharField(max_length=150)
    req_id = models.IntegerField()
    class Meta:
        db_table = 'email_verified'