from django.db import models
from django.db.models import permalink

# Create your models here.
class Invoice(models.Model):
    from schools.companies.models import Company
    company = models.ForeignKey(Company)
    start = models.DateField()
    end = models.DateField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    @permalink
    def get_absolute_url(self):
        return ('invoice-detail', None, {'object_id':str(self.pk)})
    
    @permalink
    def get_lesson_attendees_url(self):
        return ('invoice-lesson-attendees', None, {'object_id':str(self.pk)})