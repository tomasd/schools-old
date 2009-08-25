from django.db import models

# Create your models here.
class Invoice(models.Model):
    start = models.DateField()
    end = models.DateField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)