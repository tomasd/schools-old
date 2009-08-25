from django.db import models

# Create your models here.
class Student(models.Model):
    from schools.companies.models import Company
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    title = models.CharField(max_length=10, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)
    
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
        if self.title:
            return '%s, %s %s' % (self.last_name, self.first_name, self.title)
        return '%s, %s' % (self.last_name, self.first_name)
        
    @models.permalink
    def get_absolute_url(self):
        return ('student-detail', (), {
                 'object_id':str(self.pk),})
