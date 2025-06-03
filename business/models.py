from django.db import models

# Create your models here.
class Business(models.Model):
    id = models.AutoField(primary_key=True)
    business_name_id = models.IntegerField()
    business_name = models.CharField(max_length=85)
    short_name = models.CharField(max_length=85,null=True)
    rfc = models.CharField(null=True,max_length=85)
    line_of_business = models.CharField(max_length=85,null=True)
    phone_number = models.CharField(max_length=10,null=True)
    company_id = models.IntegerField()
    company_name = models.CharField(max_length=85)
    country = models.CharField(max_length=85,null=True)
    state = models.CharField(max_length=85,null=True)
    municipality = models.CharField(max_length=85,null=True)
    city = models.CharField(max_length=85,null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True)
    deleted_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.short_name

    class Meta:
        db_table = 'business'
        managed = False

class Locations(models.Model):
    id = models.AutoField(primary_key=True)
    location_id = models.IntegerField()
    location_name = models.CharField(max_length=85)
    state_register = models.CharField(max_length=85,null=True)
    phone = models.CharField(null=True,max_length=10)
    address_street = models.CharField(max_length=85,null=True)
    address_neighborhood = models.CharField(max_length=85,null=True)
    address_city = models.CharField(max_length=85,null=True)
    address_state_name = models.CharField(max_length=85, null=True)
    address_postal_code = models.CharField(max_length=5,null=True)
    representative_rfc = models.CharField(max_length=85,null=True)
    representative_curp = models.CharField(max_length=85,null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True)
    deleted_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.location_name

    class Meta:
        db_table = 'locations'
        managed = False