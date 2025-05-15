from django.db import models

# Create your models here.


class EmailVerified(models.Model):
    token = models.CharField(max_length=150)
    req_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'email_verified'