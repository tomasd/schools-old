from decimal import Decimal
from django.db import models

# Create your models here.
class Lector(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    
    title = models.CharField(max_length=10, null=True, blank=True)
    
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
        return ('lector-detail', (), {
                 'object_id':str(self.pk),})
        
    @models.permalink
    def contracts_url(self):
        return ('lector-contracts', (), {
                 'lector_id':str(self.pk),})

def lector_price(lector, course, start, end):
    hour_rates = HourRate.objects.filter(contract__start__lte=end, contract__end__gte=start, course=course)
    if not hour_rates:
        hour_rates = lector.contract_set.filter(start__lte=end, end__gte=start, hour_rate__isnull=False)

    if not hour_rates:
        raise Exception('No hour rate specified for lector %s and %s %s' % (lector, start, end))
    
    delta = end-start
    delta_hours = Decimal(delta.days*24) + Decimal(str(delta.seconds/3600.0))
    return delta_hours * hour_rates[0].hour_rate
    
class Contract(models.Model):
    contract_number = models.CharField(max_length=30, unique=True)
    lector = models.ForeignKey('Lector')
    
    hour_rate = models.DecimalField(max_digits=10, decimal_places=2)
    
    start = models.DateField()
    end = models.DateField()
    
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @models.permalink
    def get_absolute_url(self):
        return ('lector-contract-detail', (), {
                 'lector_id':str(self.lector.pk),
                 'contract_id':str(self.pk)})
    
    def __unicode__(self):
        return self.contract_number
        
        
class HourRate(models.Model):
    from schools.courses.models import Course
    contract = models.ForeignKey('Contract')   
    course = models.ForeignKey(Course)
    
    hour_rate = models.DecimalField(max_digits=10, decimal_places=2)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return unicode(self.hour_rate)