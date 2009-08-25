from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    
    ico = models.CharField(max_length=20, null=True, blank=True)
    dic = models.CharField(max_length=20, null=True, blank=True)
    ic_dph = models.CharField(max_length=20, null=True, blank=True)
    
    street = models.CharField(max_length=100, null=True, blank=True)
    postal = models.CharField(max_length=5, null=True, blank=True)
    town = models.CharField(max_length=100, null=True, blank=True)
    
    phone = models.CharField(max_length=30, null=True, blank=True)
    mobile = models.CharField(max_length=30, null=True, blank=True)
    fax = models.CharField(max_length=30, null=True, blank=True)
    www = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('company-detail', (), {
                 'object_id':str(self.pk),})
