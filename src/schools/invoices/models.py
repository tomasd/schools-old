from django.db import models

# Create your models here.
class Invoice(models.Model):
    from schools.companies.models import Company
    company = models.ForeignKey(Company)
    start = models.DateField()
    end = models.DateField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)