# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import permalink

# Create your models here.
class Classroom(models.Model):
    name = models.CharField(max_length=100)
    infinite_room = models.BooleanField(default=False)
    
    building = models.ForeignKey('Building')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('classroom-detail', (), {
                 'classroom_id':str(self.pk),
                 'building_id':str(self.building_id)})
    
class Building(models.Model): 
    name = models.CharField(max_length=100)
    
    street = models.CharField(max_length=100, null=True, blank=True)
    postal = models.CharField(max_length=5, null=True, blank=True)
    town = models.CharField(max_length=100, null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return ('building-detail', (), {'object_id':str(self.pk)})
    
    @permalink
    def get_classrooms_url(self):
        return ('classrooms', (), {'building_id':str(self.pk)})
    
    @permalink
    def get_expenses_url(self):
        return ('building-expenses', (), {'building_id':str(self.pk)})
    

class BuildingMonthExpense(models.Model):
    building = models.ForeignKey('Building')
    
    start = models.DateField()
    end = models.DateField()
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        fmt = '%d.%m.%Y'
        return u'%s - %s: %.2f €' % (format(self.start, fmt), format(self.end, fmt), self.price)
    
    @models.permalink
    def get_absolute_url(self):
        return ('building-expense-detail', (), {
                 'building_expense_id':str(self.pk),
                 'building_id':str(self.building_id)})